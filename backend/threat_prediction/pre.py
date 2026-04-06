import os
import torch
import re
from transformers import BertTokenizerFast, BertForSequenceClassification

# -----------------------------
# Text Cleaning
# -----------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# -----------------------------
# Sentence Split (for paragraphs)
# -----------------------------
def split_sentences(text):
    sentences = re.split(r'[.!?]\s*|\n+', text)
    return [s.strip() for s in sentences if s.strip()]

# -----------------------------
# SAFE sarcasm / idiom phrases (cleaned)
# -----------------------------

INTENT_WORDS = [
    "will", "going to", "gonna", "soon", "tonight",
    "tomorrow", "coming", "on the way", "wait and see"
]

TARGET_WORDS = [
    "you", "your", "u"
]

HARM_WORDS = [
    "hurt", "kill", "beat", "attack", "destroy",
    "ruin", "end", "finish", "revenge", "pay",
    "suffer", "regret", "consequences"
]

FRIENDLY_CONTEXT = [
    "come home", "come over", "visit",
    "meet", "party", "dinner",
    "hangout", "celebrate", "function"
]
SAFE_PHRASES = [
    "kill for pizza", "killed it", "you killed him", "haha you killed",
    "lol killed", "nice joke", "dead laughing", "im dead", "i'm dead",
    "this killed me", "that killed me", "you killed it bro", "bro killed it",
    "absolutely killed it", "that joke killed me", "i almost died laughing",
    "dying laughing", "this is killer", "killer performance", "killer move",
    "joke killed me", "kill you for the joke", "destroy you for the joke",
    "kill you for the food you prepared", "kill you for the worst cake you gave",
    "break my", "wreck my", "haha", "lol", "rofl", "lmao", "funny",
    "just kidding", "pranked you", "i'm joking", "joke aside"
]

# -----------------------------
# Implicit threat phrases (cleaned + deduplicated)
# -----------------------------
IMPLICIT_THREATS = [
    "won t end well", "things won't end well", "won't end well for you",
    "this won't end well", "you will regret", "you ll regret",
    "things will get ugly", "watch what happens",
    "you will see", "don t test me",
    "keep talking", "keep ignoring me",
    "i will end you", "end you", "finish you", "ruin you",
    "destroy you", "break you",
    "i will come for you", "i will find you", "i know where you live",
    "i will hurt you", "i will beat you",
    "i will make things worse", "very uncomfortable",
    "bad things will happen", "you better watch out",
    "cost you", "inviting problems", "closer to trouble",
    "kill you", "i will ruin your life",
    "things will go badly", "you won t like it",
    "watch your back", "trouble will come",
    "you will face consequences",
    "your life will get complicated",
    "don t cross me", "pay the price",
    "you won't survive this",
    "this is not over", "not a good idea",
    "shame if anyone else", "shame if someone else",
    "better watch yourself", "against you"
]

# -----------------------------
# Detection Functions
# -----------------------------
def is_blackmail(text):
    t = text.lower()

    control = any(c in t for c in [
        "or", "unless", "if you", "if you don t", "if you do not"
    ])

    exposure = any(e in t for e in [
        "share", "send", "leak", "expose", "post",
        "release", "forward", "show", "make public",
        "everyone will see", "everyone knows",
        "your family sees", "your employer sees",
        "your friends see", "everyone finds out",
        "shame if someone else", "shame if anyone else"
    ])

    sensitive = any(s in t for s in [
        "image", "photo", "video", "recording",
        "private info", "secrets", "intimate content"
    ])

    return control and (exposure or sensitive)


def is_coercion(text):
    t = text.lower()
    return any(p in t for p in [
        "you will comply", "you will do what i ask",
        "you have no choice", "do what i say",
        "you must", "you better", "you will obey"
    ])


def is_soft_threat(text):
    t = text.lower()
    return any(p in t for p in [
        "this will not end well", "you will regret",
        "watch what happens", "make it difficult for you",
        "things will go badly", "you won t like it",
        "watch your back", "trouble will come",
        "you will face consequences",
        "your life will get complicated",
        "you will pay"
    ])


def is_reputation_threat(text):
    t = text.lower()
    return any(p in t for p in [
        "ruin your reputation", "destroy your reputation",
        "expose you", "tell everyone", "make it public",
        "everyone will know", "your family will know",
        "your employer will know"
    ])


def is_non_threat_context(text):
    t = text.lower()
    return any(p in t for p in [
        "asking for attention", "posting photos",
        "she looks", "she is pretty",
        "posing for fun", "sharing memories"
    ])

def implicit_threat_score(text):
    t = text.lower()
    score = 0

    # implicit threat keywords
    if any(p in t for p in IMPLICIT_THREATS):
        score += 0.4

    # harm intent words
    if any(w in t for w in HARM_WORDS):
        score += 0.3

    # intent words (future action)
    if any(w in t for w in INTENT_WORDS):
        score += 0.2

    # target words
    if any(w in t.split() for w in TARGET_WORDS):
        score += 0.2

    # friendly context reduces score
    if any(w in t for w in FRIENDLY_CONTEXT):
        score -= 0.5

    return score
# -----------------------------
# Model Load (FIXED BUG HERE)
# -----------------------------
BASE_DIR = os.path.dirname(__file__)   # ✅ FIXED
MODEL_PATH = os.path.join(BASE_DIR, "threat_model.pt")

tokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased")

model = BertForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=2
)

state_dict = torch.load(MODEL_PATH, map_location="cpu")
model.load_state_dict(state_dict)
model.eval()

# -----------------------------
# Helper
# -----------------------------
def is_safe_phrase(text):
    return any(p in text for p in SAFE_PHRASES)


def check_implicit_threat_context(sentence):
    for phrase in IMPLICIT_THREATS:
        if phrase in sentence:
            if not is_safe_phrase(sentence):
                return True
    return False


def bert_predict(sentence):
    inputs = tokenizer(
        sentence,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=1)
        return probs[0][1].item()

# -----------------------------
# FINAL PREDICT FUNCTION
# -----------------------------
def rule_based_threat(text):
    t = text.lower()

    # Safe phrases first
    if any(p in t for p in SAFE_PHRASES):
        return "NON-THREAT", 0.05

    # Non threat context
    if is_non_threat_context(t):
        return "NON-THREAT", 0.1

    # Blackmail
    if is_blackmail(t):
        return "THREAT", 0.95

    # Coercion
    if is_coercion(t):
        return "THREAT", 0.9

    # Reputation threat
    if is_reputation_threat(t):
        return "THREAT", 0.85

    # Soft threats
    if is_soft_threat(t):
        return "THREAT", 0.75

    # Implicit threat scoring
    score = implicit_threat_score(t)
    if score > 0.5:
        return "THREAT", round(score, 2)

    return None
    
def predict(text):
    cleaned = clean_text(text)

    # Rule-based detection first
    rule_result = rule_based_threat(cleaned)
    if rule_result:
        return rule_result

    # Otherwise use BERT
    sentences = split_sentences(cleaned)
    max_score = 0

    for sent in sentences:
        score = bert_predict(sent)
        max_score = max(max_score, score)

    label = "THREAT" if max_score > 0.35 else "NON-THREAT"
    return label, round(max_score, 3)
