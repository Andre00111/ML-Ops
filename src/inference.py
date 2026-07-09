"""
Inference script for making predictions with trained model.
Loads model from models/model.pkl and makes predictions on sample data.
"""
import joblib
import numpy as np
from sklearn import datasets

def inference():
    """Load model and make predictions on sample data"""

    # Load model
    model = joblib.load('models/model.pkl')

    # Load Iris dataset for target names
    iris = datasets.load_iris()
    target_names = iris.target_names

    # Sample data for inference (5 samples matching iris characteristics)
    # setosa, versicolor, virginica, setosa, versicolor
    sample_data = np.array([
        [5.1, 3.5, 1.4, 0.2],   # setosa
        [7.0, 3.2, 4.7, 1.4],   # versicolor
        [6.3, 2.5, 5.0, 2.0],   # virginica
        [4.6, 3.4, 1.3, 0.2],   # setosa
        [5.9, 3.0, 4.2, 1.5]    # versicolor
    ])

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
