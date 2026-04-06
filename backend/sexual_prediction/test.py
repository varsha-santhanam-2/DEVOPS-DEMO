from predictor import predict
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score,confusion_matrix, classification_report

# -----------------------------
# Test Sentences
# -----------------------------
test_sentences = [
    "She is not seductive",
    "The mountain has beautiful curves",
    "That girl is useless",
    "She looks sexy today",
    "He is stupid",

    "Women are great leaders",
    "She never tries to seduce anyone",
    "This movie is sexy",
    "That female is pathetic",
    "The curves of the road are dangerous",

    "She completed her project successfully",
    "She is a crazy lady",
    "That joke was dirty",
    "Her curves are attractive",

    "He is annoying",
    "She is definitely not sexy",
    "This road curves sharply",
    "The woman was trying to seduce him",
    "She is a hardworking student",

    "That person is ugly",
    "She posted nude photos",
    "Women are too emotional",
    "This is not erotic",
    "She handled the task professionally",

    "He is dumb",
    "That girl is seductive",
    "She never acts sexy",
    "The view is beautiful",
    "That female is worthless"
]

# -----------------------------
# True Labels (Ground Truth)
# -----------------------------
true_labels = [
    "Non-Sexual",
    "Non-Sexual",
    "Non-Sexual",
    "Sexual",
    "Non-Sexual",

    "Non-Sexual",
    "Non-Sexual",
    "Sexual",
    "Non-Sexual",
    "Non-Sexual",

    "Non-Sexual",
    "Non-Sexual",
    "Sexual",
    "Sexual",

    "Non-Sexual",
    "Non-Sexual",
    "Non-Sexual",
    "Sexual",
    "Non-Sexual",

    "Non-Sexual",
    "Sexual",
    "Non-Sexual",
    "Non-Sexual",
    "Non-Sexual",

    "Non-Sexual",
    "Sexual",
    "Non-Sexual",
    "Non-Sexual",
    "Non-Sexual"
]

# -----------------------------
# Get Predictions
# -----------------------------
predicted_labels = []

for s in test_sentences:
    pred = predict(s)
    predicted_labels.append(pred)
    print(f"Sentence: {s}")
    print("Prediction:", pred)
    print("-" * 50)

# -----------------------------
# Calculate Metrics
# -----------------------------
accuracy = accuracy_score(true_labels, predicted_labels)
precision = precision_score(true_labels, predicted_labels, pos_label="Sexual")
recall = recall_score(true_labels, predicted_labels, pos_label="Sexual")
f1 = f1_score(true_labels, predicted_labels, pos_label="Sexual")
cm = confusion_matrix(true_labels, predicted_labels, labels=["Non-Sexual", "Sexual"])

print("\n📊 Evaluation Results")
print("Accuracy :", accuracy)
print("Precision:", precision)
print("Recall   :", recall)
print("F1 Score :", f1)
print("Actual Non-S  ", cm[0])
print("Actual Sexual ", cm[1])
print("\n📄 Detailed Classification Report:")
print(classification_report(true_labels, predicted_labels))