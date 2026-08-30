import streamlit as st
import pandas as pd
import requests

st.title("📊 Real-Time Data Pipeline Analytics")

api_url = "http://localhost:8000/api/v1/metrics"

st.sidebar.header("Controls")
if st.sidebar.button("Trigger ETL Cycle"):
    res = requests.post("http://localhost:8000/api/v1/trigger-etl")
    if res.status_code == 200:
        st.sidebar.success("ETL Triggered Successfully!")

try:
    res = requests.get(api_url)
    data = res.json().get("data", [])
    
    if data:
        df = pd.DataFrame(data)
        st.metric(label="Total Metrics Logged", value=len(df))
        
        st.subheader("Ingested Metrics Log")
        st.dataframe(df)
        
        st.subheader("Metric Value Trends")
        st.line_chart(df.set_index("timestamp")["value"])
    else:
        st.info("No metrics logged yet.")
except Exception as e:
    st.error(f"Could not connect to FastAPI Backend: {e}")