import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# Verbindung zur PostgreSQL-DB
import psycopg2
conn = psycopg2.connect(
    "dbname=energy user=postgres password=postgres host=localhost")
query = "SELECT timestamp, daily_avg_load_mw FROM daily_load"
df = pd.read_sql(query, conn)

# Spalten umbenennen, damit Propeht sie versteht
df.rename(columns={'timestamp': 'ds', 'daily_avg_load_mw': 'y'}, inplace=True)

# Prophet-Modell erstellen
model = Prophet()
model.fit(df)

# Prognose für die nächsten 365 Tage
future = model.make_future_dataframe(df, periods=365)
forecast = model.predict(future)

# Prognose visualisieren
model.plot(forecast)
plt.show()
