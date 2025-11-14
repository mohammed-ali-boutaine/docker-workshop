import streamlit as st
import requests
import pandas as pd
import time

API_URL = "http://fastapi:8000/data"

st.title("ETL Monitoring Dashboard")

while True:
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        st.dataframe(df)
    else:
        st.write("Waiting for data...")

    time.sleep(60)  
