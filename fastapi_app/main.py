from fastapi import FastAPI
import psycopg2
import pandas as pd

app = FastAPI()

@app.get("/data")
def get_data():
    conn = psycopg2.connect(
        dbname="etl_data",
        user="airflow",
        password="airflow",
        host="postgres"
    )
    df = pd.read_sql("SELECT * FROM etl_table", conn)
    return df.to_dict(orient="records")
