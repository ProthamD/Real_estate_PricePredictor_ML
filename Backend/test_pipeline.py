"""
Simple test: load the pipeline and make a prediction directly
without running the Flask server.
"""
import pandas as pd
from joblib import load
import os

# Load the combined pipeline
MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'Model')
PIPELINE_PATH = os.path.join(MODEL_DIR, 'pipeline_combined.joblib')

print(f"Loading pipeline from: {PIPELINE_PATH}")
pipeline = load(PIPELINE_PATH)
print(f"Pipeline loaded: {type(pipeline)}")

# Test input
test_input = {
    'CRIM': 0.00632, 'ZN': 18.0, 'INDUS': 2.31, 'CHAS': 0,
    'NOX': 0.538, 'RM': 6.575, 'AGE': 65.2, 'DIS': 4.09,
    'RAD': 1, 'TAX': 296, 'PTRATIO': 15.3, 'B': 396.9, 'LSTAT': 4.98
}

# Convert to DataFrame
input_df = pd.DataFrame([test_input])
print(f"\nInput data:\n{input_df}")

# Make prediction
prediction = pipeline.predict(input_df)[0]
print(f"\n✓ Prediction successful: ${prediction:.3f}k")
print("\nBackend is ready for deployment!")
