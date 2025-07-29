import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Vitals Dashboard", layout="wide")
st.title("📈 Patient Vitals Monitor")

# Auto-refresh every 2 seconds
st_autorefresh(interval=2000, limit=None, key="refresh")

# Load and sanitize
try:
    df = pd.read_csv("patient_data.csv", encoding="utf-8")
    df.columns = df.columns.str.strip().str.replace('\ufeff', '')
    if df.empty:
        st.warning("⚠️ Waiting for data to be generated...")
        st.stop()
except Exception as e:
    st.error(f"❌ Could not load data: {e}")
    st.stop()

# ─────────────────────────────────────────────
# 🧑 Select patient
patient_ids = df["patient_id"].unique().tolist()
selected_id = st.selectbox("Select Patient ID", patient_ids)

# Filter latest entry for selected patient
patient_data = df[df["patient_id"] == selected_id]
latest = patient_data.iloc[-1]

# 👤 Patient Profile
st.markdown("### 👤 Patient Info")
st.write(f"**Patient ID:** {latest['patient_id']}")
st.write(f"**Age:** {latest['age']}")
st.write(f"**Gender:** {latest['gender']}")
st.write(f"**Location:** {latest['location']}")
st.write(f"**Last Updated:** {latest['timestamp']}")


# 🚨 Alerts Section
st.markdown("### 🚨 Health Alerts")

# Rule-based alert logic
alerts = []

if latest["heart_rate"] > 110:
    alerts.append(f"🔴 High Heart Rate: {latest['heart_rate']} bpm")

if latest["temperature"] > 38.5:
    alerts.append(f"🔴 High Temperature: {latest['temperature']} °C")

if latest["oxygen_saturation"] < 93:
    alerts.append(f"🟠 Low Oxygen Saturation: {latest['oxygen_saturation']}%")

if latest["respiration_rate"] > 20:
    alerts.append(f"🟡 High Respiration Rate: {latest['respiration_rate']} bpm")

if alerts:
    for alert in alerts:
        st.error(alert)
else:
    st.success("✅ All vitals are within normal range.")



st.divider()

# 🩺 Live Vitals
st.markdown("### 🩺 Latest Vitals")



col1, col2, col3 = st.columns(3)
col1.metric("💓 Heart Rate", f"{latest['heart_rate']} bpm")
col2.metric("🌡️ Temperature", f"{latest['temperature']} °C")
col3.metric("🩸 Blood Pressure", latest['blood_pressure'])

col4, col5, col6 = st.columns(3)
col4.metric("🫁 Respiration Rate", f"{latest['respiration_rate']} bpm")
col5.metric("🩻 Oxygen Saturation", f"{latest['oxygen_saturation']}%")
col6.metric("📍 Room", latest["location"])



st.divider()

# 📈 Charts
st.subheader(f"📉 Vitals Trend Charts for Patient {selected_id}")

# Heart Rate Chart
st.markdown("#### 💓 Heart Rate (last 50 readings)")
st.line_chart(patient_data["heart_rate"].tail(50))

# Temperature Chart
st.markdown("#### 🌡️ Temperature (last 50 readings)")
st.line_chart(patient_data["temperature"].tail(50))

# Oxygen Saturation Chart
st.markdown("#### 🩻 Oxygen Saturation (last 50 readings)")
st.line_chart(patient_data["oxygen_saturation"].tail(50))

st.caption("Dashboard auto-refreshes every 2 seconds.")
