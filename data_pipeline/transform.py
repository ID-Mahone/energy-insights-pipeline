import pandas as pd


def transform_hourly_to_daily(df):
    print("Transformiere zu Tagesdaten...")

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.set_index("timestamp")

    # Gruppieren nach Tag (UTC), Mittelwert berechnen
    daily_df = df.resample("D").mean().dropna()

    daily_df.reset_index(inplace=True)
    daily_df = daily_df.rename(columns={"load_mw": "daily_avg_load_mw"})

    print(f"✅ {len(daily_df)} Tageszeilen generiert.")
    return daily_df
