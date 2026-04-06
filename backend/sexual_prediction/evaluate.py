import pandas as pd
import torch
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from transformers import BertTokenizerFast, BertForSequenceClassification

# -----------------------------
# Load dataset (same as training)
# -----------------------------
df = pd.read_csv("davidson.csv")
df = df[["tweet", "class"]]
df["tweet"] = df["tweet"].astype(str)

# -----------------------------
# Recreate sexual labels
# -----------------------------
sexual_keywords = [
    "sex","fuck","dick","pussy","boobs","tits",
    "ass","slut","hoe","bitch","sexy","sexual"
]

def weak_sexual_label(text):
    t = text.lower()
    return 1 if any(k in t for k in sexual_keywords) else 0

df["sexual"] = df["tweet"].apply(weak_sexual_label)

# -----------------------------
# SAME train-test split (VERY IMPORTANT)
# -----------------------------
train_texts, test_texts, train_labels, test_labels = train_test_split(
    df["tweet"].tolist(),
    df["sexual"].tolist(),
    test_size=0.2,
    stratify=df["sexual"],
    random_state=42  # must match training
)

# -----------------------------
# Load tokenizer
# -----------------------------
tokenizer = BertTokenizerFast.from_pretrained("sexual_tokenizer")

test_enc = tokenizer(
    test_texts,
    truncation=True,
    padding=True,
    max_length=128,
    return_tensors="pt"
)

# -----------------------------
# Rebuild model
# -----------------------------
model = BertForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=2
)

state_dict = torch.load("sexual_model_weights.pt", map_location="cpu")
model.load_state_dict(state_dict)
model.eval()

# -----------------------------
# Predict
# -----------------------------
with torch.no_grad():
    outputs = model(**test_enc)
    y_pred = torch.argmax(outputs.logits, dim=1).numpy()

y_true = np.array(test_labels)

# -----------------------------
# Metrics
# -----------------------------
accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)

print("\n📊 Evaluation Results")
print("Accuracy :", accuracy)
print("Precision:", precision)
print("Recall   :", recall)
print("F1 Score :", f1)

print("\nDetailed Report:")
print(classification_report(y_true, y_pred))
