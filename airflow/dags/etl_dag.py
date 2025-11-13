from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
import os

def load_csv_to_postgres():
    csv_path = "/data/input.csv"

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f" CSV introuvable à : {csv_path}")

    df = pd.read_csv(csv_path)

    engine = create_engine("postgresql://airflow:airflow@postgres:5432/etl_data")

    df.to_sql("etl_table", engine, if_exists="replace", index=False)

    print(f" {len(df)} lignes insérées dans la table 'etl_table'")

# ---------------- DAG Definition ----------------
with DAG(
    dag_id="csv_to_postgres",
    start_date=datetime(2024, 1, 1),
    schedule_interval="* * * * *",  # chaque minute
    catchup=False,
    tags=["ETL", "CSV", "Postgres"]
) as dag:

    load_csv_task = PythonOperator(
        task_id="load_csv_to_postgres",
        python_callable=load_csv_to_postgres
    )

    load_csv_task
