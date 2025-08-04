import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    roc_auc_score,
    roc_curve
)
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier
import numpy as np
import os

def evaluate_model(model, X_test, y_test, feature_names=None):
    print("📊 Evaluation Metrics:")
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)

    print(f"Accuracy: {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall: {rec:.4f}")
    print(f"F1-score: {f1:.4f}")

    os.makedirs("plots", exist_ok=True)

    # === Confusion Matrix ===
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.tight_layout()
    plt.savefig("plots/confusion_matrix.png")
    plt.close()

    # === ROC Curve ===
    try:
        y_test_bin = label_binarize(y_test, classes=np.unique(y_test))
        if hasattr(model, "predict_proba"):
            y_score = model.predict_proba(X_test)
        else:
            y_score = OneVsRestClassifier(model).fit(X_test, y_test).predict_proba(X_test)

        fpr, tpr, _ = roc_curve(y_test_bin.ravel(), y_score.ravel())
        roc_auc = roc_auc_score(y_test_bin, y_score, average="macro", multi_class="ovr")

        plt.figure()
        plt.plot(fpr, tpr, label=f"ROC Curve (AUC = {roc_auc:.4f})")
        plt.plot([0, 1], [0, 1], "k--")
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title("Multi-Class ROC Curve")
        plt.legend(loc="lower right")
        plt.tight_layout()
        plt.savefig("plots/roc_curve.png")
        plt.close()
    except Exception as e:
        print(f"⚠️ ROC AUC could not be computed: {e}")

# === Allow standalone test run ===
if __name__ == "__main__":
    print("🚀 evaluation.py started...")
