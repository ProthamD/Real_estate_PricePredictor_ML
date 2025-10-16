"""
Test script for the Flask prediction API
"""
import requests
import json

# Test data
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

try:
    # Test the /predict endpoint
    response = requests.post(
        'http://127.0.0.1:5000/predict',
        json=test_input,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        prediction = response.json().get('prediction')
        print(f"\n✓ Test passed! Predicted price: ${prediction}k")
    else:
        print(f"\n✗ Test failed with status {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("✗ Cannot connect to Flask server. Make sure it's running on http://127.0.0.1:5000")
except Exception as e:
    print(f"✗ Error: {e}")
