from fastapi import FastAPI, Query, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from forecasting.database import get_db, Forecast
from prophet import Prophet
from forecasting.auth import api_key_auth
from fastapi_limiter import FastAPILimiter 
from fastapi_limiter.depends import RateLimiter
from redis.asyncio import Redis
import os
import pandas as pd
import joblib
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Initialize Redis connection for rate limiting
redis = Redis(host="localhost", port=6379, db=0)

# Initialize the FastAPILimiter with Redis connection
@app.on_event("startup")
async def startup():
    await FastAPILimiter.init(redis)

# Absolute path to model
model_path = os.path.join(os.path.dirname(__file__), "model.pkl")

# Load the trained model
try:
    model: Prophet = joblib.load(model_path)
except Exception as e:
    print(f"❌ Failed to load model: {e}")
    model = None

@app.get("/", dependencies=[Depends(RateLimiter(times=5, seconds=60))])  # Apply rate limiting for root endpoint
async def read_root():
    return {"message": "⚡ Welcome to the Energy Forecast API!"}

@app.get("/predict", dependencies=[Depends(RateLimiter(times=5, seconds=60))])  # Apply rate limiting for predict endpoint
async def get_forecast(
    days: int = Query(default=30, ge=1, le=365),
    db: Session = Depends(get_db),
    api_key: str = Depends(api_key_auth)):

    if not model:
        logger.error("Model not loaded!")
        return JSONResponse(content={"error": "Model not loaded"}, status_code=500)

    try:
        logger.info(f"Generating forecast for {days} days")
        future = model.make_future_dataframe(periods=days)
        logger.debug(f"Future DataFrame:\n{future.head()}")

        forecast = model.predict(future)
        forecast_subset = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(days)

        # Save forecast data to DB 
        logger.info(f"Saving forecast data to DB...")
        for index, row in forecast_subset.iterrows():
            forecast_entry = Forecast(
                ds=row['ds'],
                yhat=row['yhat'],
                yhat_lower=row['yhat_lower'],
                yhat_upper=row['yhat_upper']
            )
            db.add(forecast_entry)

        db.commit()
        logger.info("Forecast data saved successfully")

        forecast_json = forecast_subset.to_dict(orient="records")
        return forecast_json

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"SQLAlchemy error: {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/get_forecasts")
async def get_forecasts(db: Session = Depends(get_db)):
    forecasts = db.query(Forecast).all()  # Get all forecast data from the table
    return [{"ds": f.ds, "yhat": f.yhat, "yhat_lower": f.yhat_lower, "yhat_upper": f.yhat_upper} for f in forecasts]
