import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from transformers import BertTokenizerFast, BertForSequenceClassification, Trainer, TrainingArguments

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv("davidson.csv")
df = df[["tweet", "class"]]
df["tweet"] = df["tweet"].astype(str)

# -----------------------------
# Weak sexual labels
# -----------------------------
sexual_keywords = [
    "sex","fuck","dick","pussy","boobs","tits",
    "ass","slut","hoe","bitch","sexy","sexual"
]

def weak_sexual_label(text):
    t = text.lower()
    return 1 if any(k in t for k in sexual_keywords) else 0

df["sexual"] = df["tweet"].apply(weak_sexual_label)

print("Label counts:")
print(df["sexual"].value_counts())

# -----------------------------
# Train / Test split
# -----------------------------
train_texts, test_texts, train_labels, test_labels = train_test_split(
    df["tweet"].tolist(),
    df["sexual"].tolist(),
    test_size=0.2,
    stratify=df["sexual"],
    random_state=42
)

# -----------------------------
# Tokenizer
# -----------------------------
MODEL = "bert-base-uncased"
tokenizer = BertTokenizerFast.from_pretrained(MODEL)

train_enc = tokenizer(train_texts, truncation=True, padding=True, max_length=128)
test_enc = tokenizer(test_texts, truncation=True, padding=True, max_length=128)

# -----------------------------
# Dataset class
# -----------------------------
class TextDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {k: torch.tensor(v[idx]) for k, v in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

train_ds = TextDataset(train_enc, train_labels)
test_ds = TextDataset(test_enc, test_labels)

# -----------------------------
# Model
# -----------------------------
model = BertForSequenceClassification.from_pretrained(MODEL, num_labels=2)

args = TrainingArguments(
    output_dir="./sexual_model",
    eval_strategy="epoch",
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    learning_rate=2e-5,
    save_strategy="epoch",
    logging_steps=100,
    fp16=torch.cuda.is_available()
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=train_ds,
    eval_dataset=test_ds
)

# -----------------------------
# Train
# -----------------------------
trainer.train()

# -----------------------------
# Save as .pt
# -----------------------------
torch.save(model.state_dict(), "sexual_model_weights.pt")
tokenizer.save_pretrained("sexual_tokenizer")


# Save weights only (optional)
torch.save(model.state_dict(), "sexual_model_weights.pt")

# Save tokenizer
tokenizer.save_pretrained("sexual_tokenizer")

print("\n✅ Training finished.")

print("✅ Weights saved as sexual_model_weights.pt")
print("✅ Tokenizer saved in sexual_tokenizer/")