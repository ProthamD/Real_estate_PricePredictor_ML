from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from joblib import load
import os

app = Flask(__name__)
CORS(app)

# Get the absolute path to the model file
MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'Model')
MODEL_PATH = os.path.join(MODEL_DIR, 'ESTATE_PRICE_CALCULATOR.joblib')


# Add file existence check
print(f"Model exists: {os.path.exists(MODEL_PATH)}")


try:
    # Load the trained model and pipeline
    model = load(MODEL_PATH)
  
    print("Model and pipeline loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")
    raise

@app.route('/')
def home():
    return "Real Estate Prediction API - Use /predict endpoint"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        
        # Validate input data
        if not data:
            return jsonify({"error": "No input data provided"}), 400
            
        # Convert input features to DataFrame
        input_data = pd.DataFrame([data])
        
        # Preprocess the input data
        input_prepared = pipeline.transform(input_data)
        
        # Make prediction
        prediction = model.predict(input_prepared)[0]
        
        return jsonify({
            "prediction": round(float(prediction), 3),
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