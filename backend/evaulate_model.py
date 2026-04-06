import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_curve, auc

# Import your prediction function
from final_prediction import final_predict


# =========================
# TEST DATA WITH 4 LABELS
# =========================
test_data = [
    ("She is sexy and dangerous", "sexual_non_threat"),
    ("I will kill you", "non_sexual_threat"),
    ("The curves of the road are dangerous", "non_sexual_non_threat"),
    ("She handled the task professionally", "non_sexual_non_threat"),
    ("You will do what I ask or I will share those private images publicly", "sexual_threat"),
    ("Send me what I asked for or I will ruin your reputation completely", "non_sexual_threat"),
    ("I have recordings of you and I will use them if you do not cooperate", "non_sexual_threat"),
    ("You will comply or your intimate photos go to your employer", "sexual_threat"),
    ("Delete your account or I will send those images to everyone you know", "non_sexual_threat"),

    ("She only got that job because of how she looks", "non_sexual_non_threat"),
    ("She must have slept her way to that position", "sexual_non_threat"),

    ("I will find you and you will regret everything you said", "non_sexual_threat"),
    ("Post that again and see how closer to trouble you are ", "non_sexual_threat"),
    ("I know where you live and I am not afraid to show up", "non_sexual_threat"),
    ("Delete your account or I will send those images to everyone you know","sexual_threat"),
    ("Any woman posting photos like that is asking for attention","sexual_threat"),

    ("You are genuinely one of the dumbest people I have encountered online", "non_sexual_non_threat"),
    ("Nobody asked for your thoughts and nobody will ever care about them", "non_sexual_non_threat"),

    ("Wow your latest pic looks tempting", "sexual_non_threat"),
    ("Oh very flirty and provocative", "sexual_non_threat"),

    ("You rejected me publicly so you will face consequences", "non_sexual_threat"),
    ("I have intimate recordings and I will leak them", "sexual_threat"),

    ("the mountain photos were awesome", "non_sexual_non_threat"),
    ("You keep ignoring my messages. If you don't reply tonight, I will post your too revealing photos everywhere. Don't test me, I am serious.","sexual_threat")
]


# =========================
# LABEL ENCODING
# =========================
label_to_int = {
    "sexual_threat": 0,
    "sexual_non_threat": 1,
    "non_sexual_threat": 2,
    "non_sexual_non_threat": 3
}

int_to_label = {v: k for k, v in label_to_int.items()}


# =========================
# RUN PREDICTIONS
# =========================
y_true = []
y_pred = []

for text, true_label in test_data:
    result = final_predict(text)
    pred_label = result["final_label"]

    y_true.append(label_to_int[true_label])
    y_pred.append(label_to_int[pred_label])


for text, true_label in test_data:
    result = final_predict(text)
    pred_label = result["final_label"]

    print("Sentence :", text)
    print("Actual   :", true_label)
    print("Predicted:", pred_label)
    print("-----------------------------------")

    y_true.append(label_to_int[true_label])
    y_pred.append(label_to_int[pred_label])

# =========================
# PERFORMANCE METRICS
# =========================
print("\n===== PERFORMANCE METRICS =====\n")

print("Accuracy :", accuracy_score(y_true, y_pred))
print("Precision:", precision_score(y_true, y_pred, average='weighted'))
print("Recall   :", recall_score(y_true, y_pred, average='weighted'))
print("F1 Score :", f1_score(y_true, y_pred, average='weighted'))

print("\nClassification Report:\n")
print(classification_report(y_true, y_pred, target_names=label_to_int.keys()))



# =========================
# CONFUSION MATRIX
# =========================
cm = confusion_matrix(y_true, y_pred)

plt.figure()
sns.heatmap(cm, annot=True, fmt="d",
            xticklabels=label_to_int.keys(),
            yticklabels=label_to_int.keys())
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.title("Confusion Matrix")
plt.show()


# =========================
# ROC CURVE (MULTICLASS)
# =========================
y_true_bin = label_binarize(y_true, classes=[0,1,2,3])

# NOTE:
# If your model does not return probabilities,
# we simulate probabilities for ROC demo
y_prob = np.random.rand(len(y_true), 4)

fpr = dict()
tpr = dict()
roc_auc = dict()

for i in range(4):
    fpr[i], tpr[i], _ = roc_curve(y_true_bin[:, i], y_prob[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])

plt.figure()

for i in range(4):
    plt.plot(fpr[i], tpr[i], label=f"{int_to_label[i]} (AUC = {roc_auc[i]:.2f})")

plt.plot([0,1],[0,1])
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend()
plt.show()