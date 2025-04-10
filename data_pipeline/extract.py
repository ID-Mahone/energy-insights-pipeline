import pandas as pd

# Quelle: Stromverbauch in Deutschland (ENTSOE), 2006-2022, stündlich
URL = "https://data.open-power-system-data.org/time_series/2020-10-06/time_series_60min_singleindex.csv"


def extract_power_data():
    print("Lade Verbrauchsdaten...")
    df = pd.read_csv(URL, parse_dates=["utc_timestamp"])
    df = df[["utc_timestamp", "DE_load_actual_entsoe_transparency"]]
    df = df.rename(columns={
        "utc_timestamp": "timestamp",
        "DE_load_actual_entsoe_transparency": "load_mw"
    })
    df = df.dropna()
    print(f"✅ {len(df)} Zeilen geladen.")
    return df


if __name__ == "__main__":
    df = extract_power_data()
    print(df.head())
