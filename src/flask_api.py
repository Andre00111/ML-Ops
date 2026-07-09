"""
Flask API for serving ML model predictions.
Loads trained model from models/model.pkl and provides REST endpoint.
"""
import joblib
import pandas as pd
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Load model on startup
MODEL_PATH = os.getenv('MODEL_PATH', 'models/model.pkl')
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model not found at {MODEL_PATH}")

model = joblib.load(MODEL_PATH)
print(f"✓ Model loaded from {MODEL_PATH}")


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'model': 'loaded'}), 200


@app.route('/predict', methods=['POST'])
def predict():
    """
    Make predictions on Iris data.

    Request JSON:
    {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }

    Response:
    {
        "prediction": 0,
        "class_name": "setosa"
    }
    """
    try:
        data = request.json

        # Validate input
        required_fields = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
        if not all(field in data for field in required_fields):
            return jsonify({
                'error': f'Missing fields. Required: {required_fields}'
            }), 400

        # Prepare features
        features = pd.DataFrame([{
            'sepal_length': float(data['sepal_length']),
            'sepal_width': float(data['sepal_width']),
            'petal_length': float(data['petal_length']),
            'petal_width': float(data['petal_width'])
        }])

        # Make prediction
        prediction = model.predict(features)[0]

        # Map to class names
        class_names = ['setosa', 'versicolor', 'virginica']
        class_name = class_names[int(prediction)]

        return jsonify({
            'prediction': int(prediction),
            'class_name': class_name,
            'confidence': 'high'  # TODO: add actual confidence scores
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/batch-predict', methods=['POST'])
def batch_predict():
    """
    Batch predictions on multiple samples.

    Request JSON:
    [
        {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2},
        {"sepal_length": 7.0, "sepal_width": 3.2, "petal_length": 4.7, "petal_width": 1.4}
    ]

    Response:
    {
        "predictions": [0, 1],
        "class_names": ["setosa", "versicolor"]
    }
    """
    try:
        data = request.json

        if not isinstance(data, list):
            return jsonify({'error': 'Request body must be a list of samples'}), 400

        # Prepare features
        features = pd.DataFrame(data)

        # Make predictions
        predictions = model.predict(features)

        # Map to class names
        class_names = ['setosa', 'versicolor', 'virginica']
        class_names_list = [class_names[int(p)] for p in predictions]

        return jsonify({
            'predictions': [int(p) for p in predictions],
            'class_names': class_names_list,
            'count': len(predictions)
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    # Development: debug=True, Production: debug=False
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    app.run(host='0.0.0.0', port=5000, debug=debug)
