import pandas as pd
from prophet import Prophet
from sqlalchemy import create_engine
import plotly.graph_objects as go
import psycopg2
import time
import os
import joblib

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
    df = pd.read_sql(query, conn)

    # Check if data is empty
    if df.empty:
        raise ValueError("DataFrame is empty. Check your database and query.")

    # Convert to UTC then remove timezone info (Prophet requirement)
    df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
    df['timestamp'] = df['timestamp'].dt.tz_localize(None)

    # Rename columns for Prophet
    df.rename(columns={'timestamp': 'ds', 'daily_avg_load_mw': 'y'}, inplace=True)

    # Check if model already exists
    model_path = "model.pkl"
    if os.path.exists(model_path):
        print("ℹ️ model.pkl already exists. Skipping training.")
        model = joblib.load(model_path)
    else:
        # Train and save the model
        model = Prophet()
        model.fit(df)
        joblib.dump(model, model_path)
        print("✅ Model trained and saved to model.pkl")

    # Generate future dataframe and forecast
    future = model.make_future_dataframe(periods=365)
    forecast = model.predict(future)

    # Create Plotly figure
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Forecast'))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'], fill=None, mode='lines',
                             line_color='gray', name='Lower Bound'))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'], fill='tonexty', mode='lines',
                             line_color='gray', name='Upper Bound'))

    fig.update_layout(
        title="Forecast: Daily Energy Load (MW)",
        xaxis_title="Date",
        yaxis_title="Load (MW)",
        template="plotly_dark"
    )

    fig.show()

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    if 'conn' in locals():
        conn.close()
        print("🔌 Database connection closed.")
