import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedShuffleSplit, cross_val_score
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
from joblib import dump, load
import matplotlib.pyplot as plt


housing = pd.read_csv("REdata.csv")
print("Data loaded successfully.")
print(f"Dataset shape: {housing.shape}")


split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
for train_index, test_index in split.split(housing, housing['CHAS']):
    strat_train_set = housing.loc[train_index]
    strat_test_set = housing.loc[test_index]

print(f"Training set size: {len(strat_train_set)}, Test set size: {len(strat_test_set)}")

housing = strat_train_set.drop("MEDV", axis=1)
housing_labels = strat_train_set["MEDV"].copy()


my_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("std_scalar", StandardScaler()),
])


housing_num_tr = my_pipeline.fit_transform(housing)
print("Data preprocessing completed.")

# --- It was before tuning it to finest ---
# model = RandomForestRegressor()
# model.fit(housing_num_tr, housing_labels)
# --- till here---

# --- After fine tuning ---
print("Model training completed.")
param_grid = {
    'n_estimators': [50, 100, 300],  
    'max_depth': [None, 10, 20],  # Maximum depth of the trees
    'min_samples_split': [2, 5]   # Minimum samples required to split a node
}

rf = RandomForestRegressor(random_state=42)

# Creating the grid search with cross-validation
print("Starting hyperparameter tuning with GridSearchCV...")
grid_search = GridSearchCV(
    estimator=rf,
    param_grid=param_grid,
    cv=5,                      # 5-fold cross-validation
    scoring='neg_mean_squared_error',
    verbose=1,                 
    n_jobs=-1                  
)

grid_search.fit(housing_num_tr, housing_labels)

best_params = grid_search.best_params_
print(f"Best parameters found: {best_params}")

# Using the best model found
model = grid_search.best_estimator_
print("Model training completed with hyperparameter tuning.")

#--- this was before tuning it to finest ---
# housing_prediction = model.predict(housing_num_tr)
# mse = mean_squared_error(housing_labels, housing_prediction)
# rmse = np.sqrt(mse)
# print(f"Training RMSE: {rmse}")


# scores = cross_val_score(model, housing_num_tr, housing_labels, 
#                         scoring="neg_mean_squared_error", cv=10)
# rmse_scores = np.sqrt(-scores)
# mean_rmse = rmse_scores.mean()
# std_rmse = rmse_scores.std()
# print(f"Cross-validation RMSE: {mean_rmse:.2f} (±{std_rmse:.2f})")


# dump(model, "ESTATE_PRICE_CALCULATOR.joblib")
# print("Model saved as 'ESTATE_PRICE_CALCULATOR.joblib'")

# ---till this it was in preprocess and not fine tuned---

X_test = strat_test_set.drop("MEDV", axis=1)
Y_test = strat_test_set["MEDV"].copy()
X_test_prepared = my_pipeline.transform(X_test)
final_prediction = model.predict(X_test_prepared)
final_mse = mean_squared_error(Y_test, final_prediction)
final_rmse = np.sqrt(final_mse)
print(f"Tuned model test RMSE: {final_rmse}")


# ---After tuning it---


tuned_housing_prediction = model.predict(housing_num_tr)
tuned_mse = mean_squared_error(housing_labels, tuned_housing_prediction)
tuned_rmse = np.sqrt(tuned_mse)
print(f"Tuned model training RMSE: {tuned_rmse}")

tuned_scores = cross_val_score(model, housing_num_tr, housing_labels, 
                        scoring="neg_mean_squared_error", cv=10)
tuned_rmse_scores = np.sqrt(-tuned_scores)
tuned_mean_rmse = tuned_rmse_scores.mean()
tuned_std_rmse = tuned_rmse_scores.std()
print(f"Tuned model cross-validation RMSE: {tuned_mean_rmse:.2f} (±{tuned_std_rmse:.2f})")


def predict_house_price(features):
    """Predict house price based on input features.
    
    Args:
        features: A dictionary with the following keys:
            - CRIM: Per capita crime rate by town
            - ZN: Proportion of residential land zoned for lots over 25,000 sq.ft.
            - INDUS: Proportion of non-retail business acres per town
            - CHAS: Charles River dummy variable (1 if tract bounds river; 0 otherwise)
            - NOX: Nitric oxides concentration (parts per 10 million)
            - RM: Average number of rooms per dwelling
            - AGE: Proportion of owner-occupied units built prior to 1940
            - DIS: Weighted distances to five Boston employment centers
            - RAD: Index of accessibility to radial highways
            - TAX: Full-value property-tax rate per $10,000
            - PTRATIO: Pupil-teacher ratio by town
            - B: 1000(Bk - 0.63)^2 where Bk is the proportion of blacks by town
            - LSTAT: % lower status of the population
    
    Returns:
        Predicted house price in $1000s
    """
    # Converting input features to DataFrame
    input_data = pd.DataFrame([features])

    input_prepared = my_pipeline.transform(input_data)
    
    prediction = model.predict(input_prepared)[0]
    
    return prediction



print("\nFeature Importance:")
feature_importances = model.feature_importances_
feature_names = housing.columns


feature_importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': feature_importances
})

# Sorting by importance
feature_importance_df = feature_importance_df.sort_values('Importance', ascending=False)
print(feature_importance_df)


try:
    plt.figure(figsize=(10, 6))
    plt.barh(feature_importance_df['Feature'], feature_importance_df['Importance'])
    plt.xlabel('Importance')
    plt.title('Feature Importance')
    plt.tight_layout()
    plt.savefig('feature_importance.png')
    print("Feature importance plot saved as 'feature_importance.png'")
except Exception as e:
    print(f"Could not create plot: {e}")


if __name__ == "__main__":
    print("\n=== Housing Price Prediction USING UCI DATASET ===\n")
    print("Please enter the following details about the house:")
    
    user_house = {}

    parameters = {
        "CRIM": {
            "description": "Per capita crime rate by town",
            "min": 0.00632, "max": 88.9762
        },
        "ZN": {
            "description": "Proportion of residential land zoned for lots over 25,000 sq.ft.",
            "min": 0.0, "max": 100.0
        },
        "INDUS": {
            "description": "Proportion of non-retail business acres per town",
            "min": 0.46, "max": 27.74
        },
        "CHAS": {
            "description": "Charles River dummy variable (1 if tract bounds river; 0 otherwise)",
            "min": 0, "max": 1
        },
        "NOX": {
            "description": "Nitric oxides concentration (parts per 10 million)",
            "min": 0.385, "max": 0.871
        },
        "RM": {
            "description": "Average number of rooms per dwelling",
            "min": 3.561, "max": 8.78
        },
        "AGE": {
            "description": "Proportion of owner-occupied units built prior to 1940",
            "min": 2.9, "max": 100.0
        },
        "DIS": {
            "description": "Weighted distances to five Boston employment centers",
            "min": 1.1296, "max": 12.1265
        },
        "RAD": {
            "description": "Index of accessibility to radial highways",
            "min": 1, "max": 24
        },
        "TAX": {
            "description": "Full-value property-tax rate per $10,000",
            "min": 187, "max": 711
        },
        "PTRATIO": {
            "description": "Pupil-teacher ratio by town",
            "min": 12.6, "max": 22.0
        },
        "B": {
            "description": "1000(Bk - 0.63)^2 where Bk is the proportion of blacks by town",
            "min": 0.32, "max": 396.9
        },
        "LSTAT": {
            "description": "% lower status of the population",
            "min": 1.73, "max": 37.97
        }
    }
    

    for param, info in parameters.items():
        while True:
            try:
                print(f"\n{param}: {info['description']}")
                print(f"Valid range: {info['min']} to {info['max']}")
                
                value = input(f"Enter value for {param} [{info['min']}-{info['max']}]: ")
                
        
                if param in ["CHAS", "RAD"]:
                    value = int(value)
                else:
                    value = float(value)
                
             
                if value < info['min'] or value > info['max']:
                    print(f"Warning: Value outside typical range. Are you sure? (y/n)")
                    confirm = input().lower()
                    if confirm != 'y':
                        continue
                
                user_house[param] = value
                break
            except ValueError:
                print("Error: Please enter a valid number.")
    
    
    print("\n=== House Details ===")
    for param, value in user_house.items():
        print(f"{param}: {value}")
    
    
    try:
        predicted_price = predict_house_price(user_house)
        print(f"\nPredicted house price: ${predicted_price:.3f}k")
    except Exception as e:
        print(f"Error making prediction: {e}")
        

    while True:
        another = input("\nWould you like to predict another house price? (y/n): ").lower()
        if another == 'y':
           
            print("\n" + "-"*50)

            print("Please run the script again to make another prediction.")
            break
        elif another == 'n':
            print("Thank you for using the Protham's Housing Price Predictor!")
            break
        else:
            print("Please enter 'y' or 'n'.")