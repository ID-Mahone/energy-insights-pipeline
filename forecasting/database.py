from sqlalchemy import create_engine, Column, Integer, String, Numeric, Date, TIMESTAMP, Enum
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from uuid import uuid4
import enum
import os

# ------------------------------------
# DATABASE CONFIG
# ------------------------------------

DATABASE_URL = "postgresql://postgres:password@localhost/energy"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# ------------------------------------
# FORECAST TABLE
# ------------------------------------
class Forecast(Base):
    __tablename__ = "forecasts"

    id = Column(Integer, primary_key=True, index=True)
    ds = Column(Date, index=True)
    yhat = Column(Numeric)
    yhat_lower = Column(Numeric)
    yhat_upper = Column(Numeric)
    created_at = Column(TIMESTAMP, default="NOW()")

# ------------------------------------
# Enum for ForecastRequest Status
# ------------------------------------
class ForecastStatus(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    done = "done"
    failed = "failed"

# ------------------------------------
# New: ForecastRequest Table
# ------------------------------------
class ForecastRequest(Base):
    __tablename__ = "forecast_requests"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    days = Column(Integer, nullable =False)
    status = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

# ------------------------------------
# Create all tables
# ------------------------------------
Base.metadata.create_all(bind=engine)

# ------------------------------------
# DB Dependency
# ------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

