from sqlalchemy import create_engine, Column, Integer, String, Numeric, Date, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = "postgresql://postgres:password@localhost/energy"

#SQLAlchemy engine and session
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Model Class
Base = declarative_base()

# Forecasts Table define
class Forecast(Base):
    __tablename__ = "forecasts"

    id = Column(Integer, primary_key=True, index=True)
    ds = Column(Date, index=True)
    yhat = Column(Numeric)
    yhat_lower = Column(Numeric)
    yhat_upper = Column(Numeric)
    created_at = Column(TIMESTAMP, default="NOW()")

Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

