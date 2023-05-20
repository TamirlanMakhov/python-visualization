import sqlite3
import pandas as pd


def get_data_from_db() -> pd.DataFrame:
    with sqlite3.connect(r'./testDB.db') as conn:
        df = pd.read_sql_query("SELECT * FROM sources", conn)
    return df
