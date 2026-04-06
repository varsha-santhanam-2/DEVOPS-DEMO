# predictor.py (Long-paragraph Context-aware Sexual Predictor)

import os
import torch
from transformers import BertTokenizerFast, BertForSequenceClassification
import re

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = os.path.dirname(__file__)
TOKENIZER_PATH = os.path.join(BASE_DIR, "sexual_tokenizer")
WEIGHTS_PATH = os.path.join(BASE_DIR, "sexual_model_weights.pt")

# -----------------------------
# Load Tokenizer & Model
# -----------------------------
tokenizer = BertTokenizerFast.from_pretrained(TOKENIZER_PATH)

MODEL_NAME = "bert-base-uncased"
model = BertForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=2
)

state_dict = torch.load(WEIGHTS_PATH, map_location="cpu")
model.load_state_dict(state_dict)
model.eval()

# -----------------------------
# Keywords & Rules
# -----------------------------
SEXUAL_WORDS = [
    "sexy", "nude", "naked", "strip", "horny", "milf", "booty",
    "jiggle", "twerking", "erotic", "seduce", "provocative",
    "lick", "ride", "busty", "orgasm", "fetish",
    "panties", "underwear", "cleavage", "seductive",
    "too hot to handle", "catching attention", "making hearts skip",
    "turning up the heat", "hotness overload", "too tempting to ignore",
    "those angles", "tempting", "naughty", "too revealing", "flirty",
    "watching a little too much", "dangerous for you",
    "without clothes", "every angle", "boss got the full view",
    "every single angle", "intimate","private", "slept her way"
]

CONTEXT_TRIGGERS = ["curves", "figure", "body"]

FEMALE_REFS = [
    "she", "her", "woman", "women",
    "girl", "girls", "lady", "female", "females"
]

NEGATIONS = [
    "not", "never", "no", "none",
    "cannot", "can't", "doesn't", "isn't"
]

SAFE_CONTEXT = [
    "measured", "covered", "clothed",
    "dressed", "modest", "safe"
]

DENY_PHRASES = [
    "never trying to",
    "not attempting to",
    "does not want to",
    "no intention to"
]

# -----------------------------
# Helper Functions
# -----------------------------
def is_negated(sentence, word, window=7):
    words = sentence.lower().split()
    for i, w in enumerate(words):
        if word in w:
            start = max(0, i - window)
            if any(n in words[start:i] for n in NEGATIONS):
                return True
    return False


def check_contextual_sexual(sentence, window=7):
    words = sentence.lower().split()
    for i, w in enumerate(words):
        if w in CONTEXT_TRIGGERS:
            start = max(0, i - window)
            end = min(len(words), i + window + 1)
            context = words[start:end]

            if any(f in context for f in FEMALE_REFS):
                if any(s in context for s in SAFE_CONTEXT + NEGATIONS):
                    continue
                if any(phrase in sentence for phrase in DENY_PHRASES):
                    continue
                return True
    return False


def split_sentences(text):
    sentences = re.split(r'[.!?]\s*|\n+', text)
    return [
        re.sub(r"[^\w\s]", " ", s.lower()).strip()
        for s in sentences if s.strip()
    ]


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
# Main Prediction Function
# -----------------------------
def predict(text: str):
    sentences = split_sentences(text)

    max_score = 0

    for sent in sentences:

        # Skip denial sentences
        if any(phrase in sent for phrase in DENY_PHRASES):
            continue

        # Explicit keyword detection
        explicit_score = 0
        for word in SEXUAL_WORDS:
            if word in sent and not is_negated(sent, word):
                explicit_score = 1.0
                break

        # Context-based detection
        context_score = 0
        if check_contextual_sexual(sent):
            context_score = 0.8

        # BERT prediction
        bert_score = bert_predict(sent)

        # Final sentence score
        sent_score = max(explicit_score, context_score, bert_score)
        max_score = max(max_score, sent_score)

    label = "Sexual" if max_score > 0.5 else "Non-Sexual"

    return label, round(max_score, 3)
