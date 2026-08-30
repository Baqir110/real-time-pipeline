import os
import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="Data Pipeline Analytics", layout="wide")
st.title("📊 Real-Time Data Pipeline Analytics")

# Dynamically pick up the Render URL, fallback to localhost for offline dev
BASE_URL = os.getenv(
    "API_URL", "https://real-time-pipeline-dashboard.onrender.com"
).rstrip("/")
API_BASE_URL = f"{BASE_URL}/api/v1"

st.sidebar.header("Controls")

# Button action to trigger ETL pipeline
if st.sidebar.button("Trigger ETL Cycle"):
    try:
        response = requests.post(f"{API_BASE_URL}/trigger-etl", timeout=10)
        if response.status_code == 200:
            st.sidebar.success("ETL Triggered Successfully!")
            st.rerun()
        else:
            st.sidebar.error(f"Failed with status code: {response.status_code}")
    except Exception as err:
        st.sidebar.error(f"Could not connect to FastAPI server: {err}")

# Fetch and display metrics from backend
col1, col2 = st.columns([1, 2])

try:
    res = requests.get(f"{API_BASE_URL}/metrics", timeout=5)
    if res.status_code == 200:
        metrics_data = res.json().get("data", [])
        if metrics_data:
            df = pd.DataFrame(metrics_data)

            with col1:
                st.metric(label="Total Metrics Logged", value=len(df))
                st.subheader("Raw Metrics")
                st.dataframe(df, use_container_width=True)

            with col2:
                st.subheader("Metric Values Over Time")
                st.line_chart(df.set_index("id")["value"])
        else:
            st.info(
                "No metrics logged yet. Click 'Trigger ETL Cycle' on the left to run the pipeline."
            )
    else:
        st.error("Failed to retrieve metrics from FastAPI.")
except Exception as e:
    st.error(
        f"FastAPI server is offline: {e}. Please ensure Uvicorn is running on the backend."
    )