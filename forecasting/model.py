import pandas as pd
from prophet import Prophet
from sqlalchemy import create_engine
import plotly.graph_objects as go  # Import plotly
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
    df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)  # Ensure the timestamp is in UTC
    df['timestamp'] = df['timestamp'].dt.tz_localize(None)  # Remove timezone information

    # Rename columns to match Prophet's expectations
    df.rename(columns={'timestamp': 'ds', 'daily_avg_load_mw': 'y'}, inplace=True)


    # Initialize and fit the model
    model = Prophet()
    model.fit(df)

    # Make future predictions
    future = model.make_future_dataframe(periods=365)
    forecast = model.predict(future)

    # Create plotly figure for interactive plotting
    fig = go.Figure()

    # Add forecast trace
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Forecast'))

    # Add confidence interval traces
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'], fill=None, mode='lines', line_color='gray', name='Lower Bound'))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'], fill='tonexty', mode='lines', line_color='gray', name='Upper Bound'))

    # Update layout for plotly
    fig.update_layout(
        title="Forecast: Daily Energy Load (MW)",
        xaxis_title="Date",
        yaxis_title="Load (MW)",
        template="plotly_dark"  # Optional: you can choose different themes
    )

    # Show the interactive plot
    fig.show()

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    if 'conn' in locals():
        conn.close()
        print("🔌 Database connection closed.")
