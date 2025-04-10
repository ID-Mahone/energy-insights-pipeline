import pandas as pd 
from sqlalchemy import create_engine

def load_to_postgres(df, table_name="daily_load"):
    print(f"💾 Lade Daten in PostgreSQL ({table_name})...")

    # Connection string für SQLAlchemy
    engine = create_engine("postgresql://test:test@postgres:5432/energy")

    # Daten in die Datenbank schreiben
    df.to_sql(table_name, engine, if_exists="replace", index=False)

    print("✅ Daten erfolgreich gespeichert.")