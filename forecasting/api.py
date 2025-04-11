from fastapi import FastAPI
from pydantic import BaseModel
from prophet import Prophet
import pandas as pd
import joblib

app = FastAPI()

# Load pre-trained model 
model = joblib.load("model.pkl")

class ForecastRequest(BaseModel):
    periods: int = 30
    freq: str = "D" #default: daily 

@app.get("/")
def root():
    return {"message": "Energy Load Forecast API is up!"}

@app.post("/forecast")
def forecast(req: ForecastRequest):
    future = model.make_future_dataframe(periods=req.periods, freq=req.freq)
    forecast = model.predict(future)
    return forecast[["ds", "yhat"]].tail(req.periods).to_dict(orient="records")