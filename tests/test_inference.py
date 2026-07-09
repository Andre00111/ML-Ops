"""
Unit tests for inference script.
"""
import pytest
import joblib
import os
import pandas as pd
from src.inference import inference
from src.train import train

def test_inference_with_saved_model():
    """Test that inference works with a saved model"""

    # Ensure model exists
    train()

    # Load model
    model = joblib.load('models/model.pkl')

    # Create sample data
    sample_data = pd.DataFrame({
        'sepal_length': [5.1, 7.0],
        'sepal_width': [3.5, 3.2],
        'petal_length': [1.4, 4.7],
        'petal_width': [0.2, 1.4]
    })

    # Make predictions
    predictions = model.predict(sample_data)

    # Assert results
    assert len(predictions) == 2, "Should return two predictions"
    assert all(p in [0, 1, 2] for p in predictions), "All predictions should be valid classes"

def test_inference_runs_without_error():
    """Test that the inference script runs without raising an exception"""

    # Ensure model exists
    train()

    # This should not raise an exception
    try:
        inference()
    except Exception as e:
        pytest.fail(f"Inference script raised exception: {e}")
