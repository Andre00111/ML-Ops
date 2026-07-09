"""
Training script for Iris classification with Logistic Regression.
Loads Iris dataset, trains model, saves to models/model.pkl
"""
import joblib
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import os

def train():
    """Load Iris, train Logistic Regression, save model"""

    # Load dataset
    iris = datasets.load_iris()
    X = iris.data
    y = iris.target

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train model
    model = LogisticRegression(
        max_iter=200,
        random_state=42
    )
    model.fit(X_train, y_train)

    # Save model
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/model.pkl')

    print(f"Model trained and saved to models/model.pkl")
    print(f"Training set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")

if __name__ == '__main__':
    train()
