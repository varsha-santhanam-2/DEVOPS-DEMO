from pre import predict as threat_predict
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix

# -----------------------------
# Test Sentences
# -----------------------------
test_sentences = [
    "I will kill you",
    "We should improve road safety",
    "I will beat you up",
    "The government announced new policies",
    "You deserve to die",
    "Let's clean our neighborhood",
    "I will destroy your house",
    "Education is important for society",
    "I will hurt you badly",
    "Community meetings help development",
    "I will shoot you",
    "Public transport needs improvement",
    "You are going to suffer",
    "Healthcare reforms are necessary",
    "I will break your legs"
]

# -----------------------------
# TRUE LABELS (Must Match Model Output Format)
# -----------------------------
true_labels = [
    "THREAT",
    "NON-THREAT",
    "THREAT",
    "NON-THREAT",
    "THREAT",
    "NON-THREAT",
    "THREAT",
    "NON-THREAT",
    "THREAT",
    "NON-THREAT",
    "THREAT",
    "NON-THREAT",
    "THREAT",
    "NON-THREAT",
    "THREAT"
]

# -----------------------------
# Get Predictions
# -----------------------------
predicted_labels = []

print("\n--- Predictions ---\n")

for sentence in test_sentences:
    label, score = threat_predict(sentence)   # unpack tuple
    predicted_labels.append(label)            # only store label

    print(f"Sentence: {sentence}")
    print(f"Prediction: {label} | Confidence: {score}")
    print("-" * 50)

# -----------------------------
# Calculate Metrics
# -----------------------------
accuracy = accuracy_score(true_labels, predicted_labels)
precision = precision_score(true_labels, predicted_labels, pos_label="THREAT")
recall = recall_score(true_labels, predicted_labels, pos_label="THREAT")
f1 = f1_score(true_labels, predicted_labels, pos_label="THREAT")

print("\n📊 Threat Model Evaluation Results")
print("Accuracy :", accuracy)
print("Precision:", precision)
print("Recall   :", recall)
print("F1 Score :", f1)

# -----------------------------
# Confusion Matrix
# -----------------------------
cm = confusion_matrix(true_labels, predicted_labels, labels=["NON-THREAT", "THREAT"])

print("\n🧾 Confusion Matrix:")
print("                 Predicted")
print("               NON-THREAT   THREAT")
print("Actual NON-THREAT ", cm[0])
print("Actual THREAT     ", cm[1])

# -----------------------------
# Classification Report
# -----------------------------
print("\n📄 Detailed Classification Report:")
print(classification_report(true_labels, predicted_labels))
