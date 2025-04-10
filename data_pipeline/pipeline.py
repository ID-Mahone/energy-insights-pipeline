from extract import extract_power_data
from transform import transform_hourly_to_daily
from load import load_to_postgres

if __name__ == "__main__":
    df_hourly = extract_power_data()
    df_daily = transform_hourly_to_daily(df_hourly)
    load_to_postgres(df_daily)
    print(df_daily.head)
