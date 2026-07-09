"""
Evaluation script for trained model.
Loads model from models/model.pkl, computes metrics, saves to results/metrics.json
"""
import joblib
import json
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
import os

def evaluate():
    """Load model and evaluate on Iris test set"""

    # Load dataset (same split as training)
    iris = datasets.load_iris()
    X = iris.data
    y = iris.target
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Load model
    model = joblib.load('models/model.pkl')

    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_test, y_pred, average=None
    )

    # Prepare metrics
    metrics = {
        'accuracy': float(accuracy),
        'precision': [float(p) for p in precision],
        'recall': [float(r) for r in recall],
        'f1': [float(f) for f in f1],
        'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
    }

    # Save metrics
    os.makedirs('results', exist_ok=True)
    with open('results/metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2)

    print(f"Evaluation complete")
    print(f"Accuracy: {accuracy:.4f}")
    for i, (p, r, f) in enumerate(zip(precision, recall, f1)):
        print(f"Class {i}: P={p:.3f}, R={r:.3f}, F1={f:.3f}")

    # Validation: fail if accuracy < 0.70
    if accuracy < 0.70:
        raise ValueError(f"Accuracy {accuracy:.4f} is below threshold 0.70")

    print("✓ Accuracy above threshold (0.70)")

if __name__ == '__main__':
    evaluate()
