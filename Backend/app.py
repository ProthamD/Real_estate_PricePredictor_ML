from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from joblib import load
import os

app = Flask(__name__)
CORS(app)

# Load the combined pipeline (preprocessing + model)
MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'Model')
PIPELINE_PATH = os.path.join(MODEL_DIR, 'pipeline_combined.joblib')

print(f"Pipeline exists: {os.path.exists(PIPELINE_PATH)}")

try:
    pipeline = load(PIPELINE_PATH)
    print("Combined pipeline loaded successfully")
    print(f"Pipeline type: {type(pipeline)}")
except Exception as e:
    print(f"Error loading pipeline: {e}")
    raise

@app.route('/')
def home():
    return "Real Estate Prediction API - Use /predict endpoint"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        
        if not data:
            return jsonify({"error": "No input data provided"}), 400
            
        # Define the correct feature order (as used during training)
        feature_order = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT']
        
        # Convert input to DataFrame with correct column order
        input_data = pd.DataFrame([data], columns=feature_order)
        
        # Use the combined pipeline (preprocessing + prediction)
        prediction = pipeline.predict(input_data)[0]
        
        # Convert prediction to thousands (model predicts in $1000s)
        prediction_value = float(prediction) * 1000
        
        return jsonify({
            "prediction": round(prediction_value, 3),
            "status": "success"
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route('/predict', methods=['GET'])
def predict_get():
    return jsonify({
        "message": "Please use POST method with housing data",
        "example_request": {
            "CRIM": 0.00632,
            "ZN": 18,
            "INDUS": 2.31,
            # ... other features
        }
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)