"""
Script to create and save a combined pipeline (preprocessing + model)
for deployment. This ensures the backend can load a single artifact
that handles both preprocessing and prediction.
"""
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from joblib import load, dump

# Load the trained model
model = load("Model/ESTATE_PRICE_CALCULATOR.joblib")
print(f"Loaded model: {type(model)}")

# Recreate the preprocessing pipeline used during training
preprocessing_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("std_scalar", StandardScaler()),
])

# Load training data to fit the preprocessing pipeline
# (must match the exact data used during model training)
housing = pd.read_csv("Model/REdata.csv")

# Split data the same way as in training
from sklearn.model_selection import StratifiedShuffleSplit
split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
for train_index, test_index in split.split(housing, housing['CHAS']):
    strat_train_set = housing.loc[train_index]

# Prepare features (drop target)
housing_features = strat_train_set.drop("MEDV", axis=1)

# Fit the preprocessing pipeline on training data
preprocessing_pipeline.fit(housing_features)
print("Preprocessing pipeline fitted on training data")

# Create a combined pipeline: preprocessing + model
combined_pipeline = Pipeline([
    ("preprocessing", preprocessing_pipeline),
    ("model", model)
])

# Save the combined pipeline
output_path = "Model/pipeline_combined.joblib"
dump(combined_pipeline, output_path)
print(f"Combined pipeline saved to: {output_path}")

# Test the combined pipeline
test_input = {
    'CRIM': 0.00632,
    'ZN': 18.0,
    'INDUS': 2.31,
    'CHAS': 0,
    'NOX': 0.538,
    'RM': 6.575,
    'AGE': 65.2,
    'DIS': 4.0900,
    'RAD': 1,
    'TAX': 296,
    'PTRATIO': 15.3,
    'B': 396.90,
    'LSTAT': 4.98
}

test_df = pd.DataFrame([test_input])
test_prediction = combined_pipeline.predict(test_df)[0]
print(f"\nTest prediction: ${test_prediction:.3f}k")
print("Combined pipeline is working correctly!")
