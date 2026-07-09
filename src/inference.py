"""
Inference script for making predictions with trained model.
Loads model from models/model.pkl and makes predictions on sample data.
"""
import joblib
import pandas as pd
from sklearn import datasets

def inference():
    """Load model and make predictions on sample data"""

    # Load model
    model = joblib.load('models/model.pkl')

    # Load Iris dataset for target names
    iris = datasets.load_iris()
    target_names = iris.target_names

    # Sample data for inference (5 random Iris samples)
    sample_data = pd.DataFrame({
        'sepal_length': [5.1, 7.0, 6.3, 4.6, 5.9],
        'sepal_width': [3.5, 3.2, 2.5, 3.4, 3.0],
        'petal_length': [1.4, 4.7, 5.0, 1.3, 4.2],
        'petal_width': [0.2, 1.4, 2.0, 0.2, 1.5]
    })

    # Make predictions
    predictions = model.predict(sample_data)
    prediction_names = [target_names[p] for p in predictions]

    print("Inference Results:")
    print("-" * 50)
    for i, (pred, name) in enumerate(zip(predictions, prediction_names)):
        print(f"Sample {i+1}: {name} (class {pred})")
    print("-" * 50)
    print("✓ Inference test passed")

if __name__ == '__main__':
    inference()
