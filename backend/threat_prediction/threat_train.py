import torch
import re
from datasets import load_dataset
from transformers import BertTokenizerFast, BertForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split

# -----------------------
# Clean text
# -----------------------
def clean_text(t):
    t = t.lower()
    t = re.sub(r"[^\w\s]", "", t)
    t = re.sub(r"\s+", " ", t)
    return t.strip()

# -----------------------
# Load Civil Comments
# -----------------------
dataset = load_dataset("civil_comments")

df = dataset["train"].to_pandas()

# Keep only text + threat
df = df[["text","threat"]]

# Convert threat to 0/1
df["label"] = df["threat"].apply(lambda x: 1 if x > 0 else 0)

# Clean
df["text"] = df["text"].astype(str).apply(clean_text)

# Small subset for Colab speed
df = df.sample(12000, random_state=42)

train_df, val_df = train_test_split(df, test_size=0.1)

# -----------------------
# BERT Base
# -----------------------
MODEL = "bert-base-uncased"

tokenizer = BertTokenizerFast.from_pretrained(MODEL)
model = BertForSequenceClassification.from_pretrained(MODEL, num_labels=2)

# -----------------------
# Tokenize
# -----------------------
def tokenize(batch):
    return tokenizer(
        batch["text"],
        padding="max_length",
        truncation=True,
        max_length=64
    )

from datasets import Dataset

train_ds = Dataset.from_pandas(train_df).map(tokenize, batched=True)
val_ds = Dataset.from_pandas(val_df).map(tokenize, batched=True)

train_ds.set_format("torch", columns=["input_ids","attention_mask","label"])
val_ds.set_format("torch", columns=["input_ids","attention_mask","label"])

# -----------------------
# Training args
# -----------------------
args = TrainingArguments(
    output_dir="./threat",
    eval_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    load_best_model_at_end=True,
    fp16=torch.cuda.is_available(),
    logging_steps=50
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=train_ds,
    eval_dataset=val_ds
)

# -----------------------
# Train
# -----------------------
trainer.train()

# -----------------------
# Save as .pt
# -----------------------
torch.save(model.state_dict(), "threat_model.pt")
tokenizer.save_pretrained("tokenizer")

print("✅ Threat model saved")
