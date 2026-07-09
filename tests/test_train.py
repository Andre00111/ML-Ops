"""
Unit tests for training script.
"""
import pytest
import joblib
import os
from sklearn.linear_model import LogisticRegression
from src.train import train

def test_train_creates_model():
    """Test that training creates a valid model.pkl file"""

    # Remove old model if exists
    model_path = 'models/model.pkl'
    if os.path.exists(model_path):
        os.remove(model_path)

    # Run training
    train()

    # Assert model file exists
    assert os.path.exists(model_path), "model.pkl was not created"

def test_model_is_valid():
    """Test that saved model can be loaded and is a LogisticRegression"""

    # Ensure model exists
    train()

    # Load model
    model = joblib.load('models/model.pkl')

    # Assert it's the right type
    assert isinstance(model, LogisticRegression), "Loaded model is not LogisticRegression"

def test_model_can_predict():
    """Test that loaded model can make predictions"""

    # Ensure model exists
    train()

    # Load model
    model = joblib.load('models/model.pkl')

    # Create sample data (4 features for Iris)
    sample = [[5.1, 3.5, 1.4, 0.2]]

    # Make prediction
    prediction = model.predict(sample)

    # Assert prediction is valid
    assert len(prediction) == 1, "Should return one prediction"
    assert prediction[0] in [0, 1, 2], "Prediction should be a valid Iris class (0, 1, or 2)"
