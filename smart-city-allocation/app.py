import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
import streamlit.components.v1 as components
import os

# Set page layout to wide for better visualization
st.set_page_config(page_title="Smart City Dashboard", layout="wide")

# Title
st.title("Smart City Resource Allocation — Udaipur")

# Load data and models
@st.cache_data
def load_data():
    traffic_clean = pd.read_csv('data/traffic_clean.csv')
    waste_clean = pd.read_csv('data/waste_clean.csv')
    emergency = pd.read_csv('data/emergency_data.csv')
    
    # Raw data for LabelEncoder mapping
    traffic_raw = pd.read_csv('data/traffic_data.csv')
    waste_raw = pd.read_csv('data/waste_data.csv')
    
    return traffic_clean, waste_clean, emergency, traffic_raw, waste_raw

@st.cache_resource
def load_models():
    traffic_model = joblib.load('traffic_model.pkl')
    waste_model = joblib.load('waste_model.pkl')
    return traffic_model, waste_model

try:
    traffic_clean, waste_clean, emergency, traffic_raw, waste_raw = load_data()
    traffic_model, waste_model = load_models()
except Exception as e:
    st.error(f"Error loading data or models: {e}")
    st.stop()

# Initialize Encoders based on raw data
le_junction = LabelEncoder()
le_junction.fit(traffic_raw['junction'].astype(str))

le_weather = LabelEncoder()
le_weather.fit(traffic_raw['weather'].astype(str))

le_area = LabelEncoder()
le_area.fit(waste_raw['area'].astype(str))

le_density = LabelEncoder()
le_density.fit(waste_raw['population_density'].astype(str))

# Section 1: Traffic Prediction
st.header("Section 1: Traffic Prediction")
col1, col2, col3 = st.columns(3)
with col1:
    hour = st.slider("Hour (0-23)", 0, 23, 12)
with col2:
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day = st.selectbox("Day of Week", days)
    day_enc = days.index(day)
with col3:
    junction = st.selectbox("Junction", sorted(traffic_raw['junction'].unique()))
    junction_enc = le_junction.transform([junction])[0]

# Add dummy values for missing model features
weather_enc = le_weather.transform(['Clear'])[0] if 'Clear' in le_weather.classes_ else 0
vehicles = int(traffic_raw['vehicles'].mean())

if st.button("Predict Traffic"):
    input_data = pd.DataFrame([[hour, day_enc, junction_enc, weather_enc, vehicles]], 
                              columns=['hour', 'day_enc', 'junction_enc', 'weather_enc', 'vehicles'])
    pred = traffic_model.predict(input_data)[0]
    if pred == 1:
        st.error("⚠️ High Congestion Expected!")
        st.warning("Recommendation: Deploy traffic police and divert heavy vehicles immediately.")
    else:
        st.success("✅ Normal Traffic Flow.")
        st.info("Recommendation: Standard monitoring procedures.")

st.markdown("---")

# Section 2: Waste Prediction
st.header("Section 2: Waste Prediction")
col4, col5, col6 = st.columns(3)
with col4:
    area = st.selectbox("Area", sorted(waste_raw['area'].unique()))
    area_enc = le_area.transform([area])[0]
with col5:
    density = st.selectbox("Population Density", sorted(waste_raw['population_density'].unique()))
    density_enc = le_density.transform([density])[0]
with col6:
    days_since = st.slider("Days Since Last Collection", 1, 7, 4)

# Default to Monday and average bin fill
if st.button("Predict Waste Overflow"):
    input_data = pd.DataFrame([[area_enc, 0, density_enc, days_since, 50]], 
                              columns=['area', 'day_of_week', 'population_density', 'last_collection_days', 'bin_fill_pct'])
    pred = waste_model.predict(input_data)[0]
    if pred == 1:
        st.error("⚠️ Overflow Risk Detected!")
        st.warning("Recommendation: Schedule an immediate waste collection truck for this area.")
    else:
        st.success("✅ Normal Bin Levels.")
        st.info("Recommendation: Maintain standard collection schedule.")

st.markdown("---")

# Section 3: Emergency Bar Chart
st.header("Section 3: Emergency Metrics")
st.write("Total incidents reported per zone.")
incident_counts = emergency.groupby('zone')['incident_count'].sum().sort_values()
st.bar_chart(incident_counts)
st.write("**Recommendation:** Assign standby ambulances and police patrol units to the zones with the highest historical incident counts.")

st.markdown("---")

# Section 4: Key Metrics Dashboard (Two Bar Charts)
st.header("Section 4: Key Metrics")
c1, c2 = st.columns(2)
with c1:
    st.subheader("Avg Congestion Score by Junction")
    avg_congestion = traffic_raw.groupby('junction')['congestion_score'].mean().sort_values()
    st.bar_chart(avg_congestion)
with c2:
    st.subheader("Avg Bin Fill % by Area")
    avg_fill = waste_raw.groupby('area')['bin_fill_pct'].mean().sort_values()
    st.bar_chart(avg_fill)

st.markdown("---")

# Section 5: Embed Map
st.header("Section 5: Live City Map")
if os.path.exists('map.html'):
    with open('map.html', 'r', encoding='utf-8') as f:
        map_html = f.read()
    components.html(map_html, height=500)
else:
    st.warning("map.html not found. Please ensure generate_map.py has been run successfully.")
