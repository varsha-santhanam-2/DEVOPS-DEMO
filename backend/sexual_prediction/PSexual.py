import os
import torch
from transformers import BertTokenizerFast, BertForSequenceClassification
import re

BASE_DIR = os.path.dirname(__file__)
TOKENIZER_PATH = os.path.join(BASE_DIR, "sexual_tokenizer")
WEIGHTS_PATH = os.path.join(BASE_DIR, "sexual_model_weights.pt")

tokenizer = BertTokenizerFast.from_pretrained(TOKENIZER_PATH)

MODEL_NAME = "bert-base-uncased"
model = BertForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=2
)

state_dict = torch.load(WEIGHTS_PATH, map_location="cpu")
model.load_state_dict(state_dict)
model.eval()

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

def predict(text: str):
    sentences = split_sentences(text)

    max_score = 0

    for sent in sentences:
        score = bert_predict(sent)
        max_score = max(max_score, score)

    label = "Sexual" if max_score > 0.5 else "Non-Sexual"

    return label, round(max_score, 3)
