from fastapi import FastAPI, Query, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from forecasting.database import get_db, Forecast
from prophet import Prophet
import os
import pandas as pd
import joblib
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



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
        logger.error("Model not loaded!")
        return JSONResponse(content={"error": "Model not loaded"}, status_code=500)

    try:
        logger.info(f"Generating forecast for {days} days")
        future = model.make_future_dataframe(periods=days)
        logger.debug(f"Future DataFrame:\n{future.head()}")

        forecast = model.predict(future)
        forecast_subset = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(days)

        #Save forecast data to DB 
        logger.info(f"Saving forecast data to DB...")
        for index, row in forecast_subset.iterrows():
            db.add(forecast(ds=row['ds'], yhat=row['yhat'], yhat_lower=row['yhat_lower'], yhat_upper=row['yhat_upper']))

        db.commit()
        logger.info("Forecast data saved successfully")

        forecast_json = forecast_subset.to_dict(orient="records")
        return forecast_json

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"SQLAlchemy error: {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

    except Exception as e:
        logger.error(f"Unexpected error: {strg(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/get_forecasts")
def get_forecasts(db: Session = Depends(get_db)):
    forecasts = db.query(Forecast).all()  # Get all forecast data from the table
    return [{"ds": f.ds, "yhat": f.yhat, "yhat_lower":f.yhat_lower,"yhat_upper":f.yhat_upper} for f in forecasts]
