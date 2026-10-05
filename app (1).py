
import streamlit as st
import pandas as pd
import joblib

# Page settings
st.set_page_config(
    page_title="Ogun AI Climate Risk Monitor",
    page_icon="🌍",
    layout="wide"
)

# Load trained model
model = joblib.load("ogun_climate_risk_model.pkl")

# Title
st.title("🌍 Ogun AI Climate Risk Monitor")

st.write(
    "An AI-assisted climate risk monitoring prototype "
    "for Ogun State, Nigeria."
)

st.divider()

# Sidebar
st.sidebar.header("Climate Conditions")

location = st.sidebar.selectbox(
    "Select Location",
    [
        "Abeokuta",
        "Ijebu-Ode",
        "Sagamu",
        "Ota",
        "Ilaro"
    ]
)

temperature = st.sidebar.number_input(
    "Temperature (°C)",
    value=27.0
)

humidity = st.sidebar.number_input(
    "Humidity (%)",
    min_value=0.0,
    max_value=100.0,
    value=80.0
)

precipitation = st.sidebar.number_input(
    "Current Rainfall (mm)",
    min_value=0.0,
    value=50.0
)

wind_speed = st.sidebar.number_input(
    "Wind Speed",
    min_value=0.0,
    value=10.0
)

soil_moisture = st.sidebar.number_input(
    "Soil Moisture",
    min_value=0.0,
    value=0.30
)

rainfall_3day = st.sidebar.number_input(
    "3-Day Rainfall (mm)",
    min_value=0.0,
    value=100.0
)

rainfall_7day = st.sidebar.number_input(
    "7-Day Rainfall (mm)",
    min_value=0.0,
    value=150.0
)

soil_moisture_3day = st.sidebar.number_input(
    "3-Day Average Soil Moisture",
    min_value=0.0,
    value=0.30
)

# Prediction
if st.button("🔍 Predict Climate Risk"):

    input_data = pd.DataFrame({
        "temperature": [temperature],
        "humidity": [humidity],
        "precipitation": [precipitation],
        "wind_speed": [wind_speed],
        "soil_moisture": [soil_moisture],
        "rainfall_3day": [rainfall_3day],
        "rainfall_7day": [rainfall_7day],
        "soil_moisture_3day": [soil_moisture_3day]
    })

    prediction = model.predict(input_data)[0]

    risk_names = {
        0: "LOW",
        1: "MODERATE",
        2: "HIGH"
    }

    risk = risk_names[prediction]

    st.subheader(f"Climate Risk — {location}")

    if risk == "HIGH":
        st.error("🔴 HIGH CLIMATE RISK")

    elif risk == "MODERATE":
        st.warning("🟠 MODERATE CLIMATE RISK")

    else:
        st.success("🟢 LOW CLIMATE RISK")

    st.write(
        f"The machine-learning model classified the "
        f"current conditions as **{risk} risk**."
    )

    st.divider()

    st.subheader("Climate Conditions")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Rainfall", f"{precipitation:.1f} mm")
    col2.metric("Temperature", f"{temperature:.1f} °C")
    col3.metric("Humidity", f"{humidity:.1f}%")
    col4.metric("Soil Moisture", f"{soil_moisture:.2f}")

    st.subheader("AI-Assisted Interpretation")

    if risk == "HIGH":
        explanation = (
            "The model classified the current conditions as "
            "high climate risk. Elevated accumulated rainfall "
            "and/or soil moisture are contributing to the "
            "classification."
        )

    elif risk == "MODERATE":
        explanation = (
            "The model classified the current conditions as "
            "moderate climate risk. Some climate indicators "
            "are elevated."
        )

    else:
        explanation = (
            "The model classified the current conditions as "
            "low climate risk based on the supplied climate indicators."
        )

    st.info(explanation)

st.divider()

st.caption(
    "Prototype for climate-risk analysis. "
    "This is not an official flood-warning system."
)
