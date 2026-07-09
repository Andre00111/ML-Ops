"""
Inference script for Iris classification.
Loads saved model and makes predictions on sample data.
"""
import joblib
import pandas as pd
from sklearn import datasets

def inference():
    """Load model and make predictions on sample data"""

    # Load model
    model = joblib.load('models/model.pkl')

    # Load Iris dataset
    iris = datasets.load_iris()

    # Create sample DataFrame (first 5 samples)
    sample_data = pd.DataFrame(
        iris.data[:5],
        columns=['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    )

    # Make predictions
    predictions = model.predict(sample_data)

    print("Sample predictions:")
    for i, pred in enumerate(predictions):
        print(f"  Sample {i+1}: {iris.target_names[pred]}")

    return predictions

if __name__ == '__main__':
    inference()
