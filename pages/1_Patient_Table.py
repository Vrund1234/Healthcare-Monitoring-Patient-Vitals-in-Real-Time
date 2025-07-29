import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Vitals Table", layout="wide")
st.title("🧾 All Patient Vitals")

# Auto-refresh
st_autorefresh(interval=2000, limit=None, key="refresh")

# Load data
df = pd.read_csv("patient_data.csv")
df.columns = df.columns.str.strip().str.replace('\ufeff', '')

# Optional filters
with st.expander("🔍 Filter Patients"):
    patient_ids = df["patient_id"].unique().tolist()
    selected = st.multiselect("Filter by Patient ID", patient_ids, default=patient_ids)
    filtered = df[df["patient_id"].isin(selected)]

# Display
st.dataframe(filtered.sort_values("timestamp", ascending=False), use_container_width=True)

# Download
csv = filtered.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download Filtered Data", csv, "filtered_vitals.csv", "text/csv")
