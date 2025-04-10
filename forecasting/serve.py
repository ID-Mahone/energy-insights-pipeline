from fastapi import FastAPI, Query, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from forecasting.database import get_db, Forecast
from prophet import Prophet
import os
import pandas as pd
import joblib


app = FastAPI()

# Absolute path to model
model_path = os.path.join(os.path.dirname(__file__), "model.pkl")

# Load the trained model
try:
    model: Prophet = joblib.load(model_path)
except Exception as e:
    print(f"❌ Failed to load model: {e}")
    model = None

@app.get("/")
def read_root():
    return {"message": "⚡ Welcome to the Energy Forecast API!"}

@app.get("/predict")
def get_forecast(days: int = Query(default=30, ge=1, le=365)):
    if not model:
        return JSONResponse(content={"error": "Model not loaded"}, status_code=500)

    try:
        future = model.make_future_dataframe(periods=days)
        forecast = model.predict(future)
        forecast_subset = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(days)
        forecast_json = forecast_subset.to_dict(orient="records")
        return forecast_json
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/get_forecasts")
def get_forecasts(db: Session = Depends(get_db)):
    forecasts = db.query(Forecast).all()  # Get all forecast data from the table
    return forecasts
