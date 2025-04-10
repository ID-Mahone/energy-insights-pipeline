import pandas as pd
from prophet import Prophet
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import psycopg2
import time
import os

def connect_db(retries=5, delay=5):
    """Establish database connection with retry logic"""
    for i in range(retries):
        try:
            conn = psycopg2.connect(
                dbname=os.getenv("DB_NAME", "energy"),
                user=os.getenv("DB_USER", "test"),
                password=os.getenv("DB_PASS", "test"),
                host=os.getenv("DB_HOST", "localhost"),
                port=os.getenv("DB_PORT", "5432")
            )
            print("✅ Database connection successful!")
            return conn
        except psycopg2.OperationalError as e:
            print(f"⚠️ Attempt {i+1}/{retries} failed: {e}")
            if i == retries - 1:
                raise
            time.sleep(delay)

try:
    # Connect to database
    conn = connect_db()
    
    # Load data
    query = "SELECT timestamp, daily_avg_load_mw FROM daily_load"

    # Read from DB
    df = pd.read_sql(query, conn)

    # Check if data is empty
    if df.empty:
        raise ValueError("DataFrame is empty. Check your database and query.")

    # Format data for Prophet
    df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)  # Make sure timestamp is UTC-aware
    df['timestamp'] = df['timestamp'].dt.tz_localize(None)  # Remove timezone information (make it naive)

    # Rename columns for Prophet
    df.rename(columns={'timestamp': 'ds', 'daily_avg_load_mw': 'y'}, inplace=True)

    # Initialize and fit the model
    model = Prophet()
    model.fit(df)

    # Make future predictions
    future = model.make_future_dataframe(periods=365)
    forecast = model.predict(future)

    # Plot the forecast
    fig = model.plot(forecast)
    plt.title("Forecast: Daily Energy Load (MW)")
    plt.xlabel("Date")
    plt.ylabel("Load (MW)")
    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    if 'conn' in locals():
        conn.close()
        print("🔌 Database connection closed.")
