import os
import torch
import re
from transformers import BertTokenizerFast, BertForSequenceClassification

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def split_sentences(text):
    sentences = re.split(r'[.!?]\s*|\n+', text)
    return [s.strip() for s in sentences if s.strip()]

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "threat_model.pt")

tokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased")

model = BertForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=2
)

state_dict = torch.load(MODEL_PATH, map_location="cpu")
model.load_state_dict(state_dict)
model.eval()

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

def predict(text):
    cleaned = clean_text(text)
    sentences = split_sentences(cleaned)

    max_score = 0

    for sent in sentences:
        score = bert_predict(sent)
        max_score = max(max_score, score)

    label = "THREAT" if max_score > 0.4 else "NON-THREAT"
    return label, round(max_score, 3)
