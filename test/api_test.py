import sys
import os

# Add the forecasting folder to the sys.path to import 'serve' from sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../forecasting')))

import joblib
from fastapi.testclient import TestClient
from serve import app  # Now it should be able to find 'serve.py' in the forecasting folder

# Load the pre-trained model (adjust the model path to account for the location of the test file)
model_path = os.path.join(os.path.dirname(__file__), '../forecasting/model.pkl')
print(f"Loading model from: {model_path}")
try:
    model = joblib.load(model_path)
    print("Model loaded successfully")
except Exception as e:
    print(f"Failed to load model: {e}")

client = TestClient(app)

def test_forecast():
    print("Sending forecast request...")
    response = client.get("/predict?days=7")  # Example with 7 days forecast
    print(f"Response status code: {response.status_code}")
    print(f"Response JSON: {response.json()}")
    assert response.status_code == 200
    assert "yhat" in response.json()[0]  # Adjust based on your response structure

# Run the test
test_forecast()
