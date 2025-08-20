import warnings
warnings.filterwarnings("ignore", message=".*ScriptRunContext.*")

import streamlit as st
import joblib
import numpy as np
import matplotlib.pyplot as plt

# ========== CONFIG ==========
st.set_page_config(
    page_title="🌱 Fertilizer Recommendation System",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== LOAD MODEL ==========
model = joblib.load("fertilizer_model.pkl")

# ========== STYLING ==========
st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        font-size: 42px;
        color: #2e7d32;
        font-weight: bold;
    }
    .sub-title {
        text-align: center;
        font-size: 20px;
        color: #555;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ========== HEADER ==========
st.markdown("<h1 class='main-title'>🌱 Smart Fertilizer Recommendation</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>AI-powered soil, water & environment analysis 🚜</p>", unsafe_allow_html=True)
st.write("---")

# ========== SIDEBAR ==========
st.sidebar.header("📊 Input Soil & Climate Data")
Soil_Moisture = st.sidebar.slider("Soil Moisture (%)", 0, 100, 50)
N = st.sidebar.number_input("Nitrogen (N)", min_value=0, max_value=200, value=50)
P = st.sidebar.number_input("Phosphorus (P)", min_value=0, max_value=200, value=50)
K = st.sidebar.number_input("Potassium (K)", min_value=0, max_value=200, value=50)
Temperature = st.sidebar.slider("Temperature (°C)", 10.0, 50.0, 25.0)
Humidity = st.sidebar.slider("Humidity (%)", 20.0, 100.0, 60.0)

# ========== FERTILIZER LOGIC ==========
fertilizers = {
    "Urea": {"N": 46, "P": 0, "K": 0},
    "DAP": {"N": 18, "P": 46, "K": 0},
    "MOP": {"N": 0, "P": 0, "K": 60},
    "NPK": {"N": 15, "P": 15, "K": 15},
}

def recommend_fertilizer(n, p, k, moisture):
    if n < 40:
        fert, amt = "Urea", 50
    elif p < 40:
        fert, amt = "DAP", 40
    elif k < 40:
        fert, amt = "MOP", 30
    else:
        fert, amt = "NPK", 25

    # Water recommendation logic
    if moisture < 30:
        water = "💧 High irrigation needed (~20-25 L/m²)"
    elif 30 <= moisture <= 60:
        water = "💦 Moderate irrigation (~10-15 L/m²)"
    else:
        water = "🌤️ No extra irrigation required"

    return fert, amt, water

# ========== PREDICTION ==========
if st.sidebar.button("🔍 Predict Fertilizer Need"):
    sample = np.array([[Soil_Moisture, N, P, K, Temperature, Humidity]])
    prediction = model.predict(sample)

    st.subheader("📌 Prediction Result")
    if prediction[0] == 1:
        fert, amount, water_need = recommend_fertilizer(N, P, K, Soil_Moisture)
        st.success(f"🌱 Fertilizer Needed: **{fert} ({amount} kg/acre)** ✅")
        st.info(f"💧 Water Supply Recommendation: {water_need}")
    else:
        st.info("🌾 Fertilizer is **Not Needed** ❌")
        fert, amount, water_need = None, None, None

    # Show input summary
    st.write("### 🌍 Input Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Soil Moisture", f"{Soil_Moisture}%")
        st.metric("Nitrogen (N)", f"{N}")
    with col2:
        st.metric("Phosphorus (P)", f"{P}")
        st.metric("Potassium (K)", f"{K}")
    with col3:
        st.metric("Temperature", f"{Temperature} °C")
        st.metric("Humidity", f"{Humidity}%")

    # ========== BAR CHART ==========
    st.write("### 📊 Soil Nutrient Levels")
    fig, ax = plt.subplots(figsize=(4,3))  # ✅ smaller chart
    nutrients = ["Nitrogen (N)", "Phosphorus (P)", "Potassium (K)"]
    values = [N, P, K]
    ax.bar(nutrients, values, color=["#66bb6a", "#42a5f5", "#ffb300"])
    ax.set_ylabel("Level")
    ax.set_title("NPK Nutrient Comparison")
    st.pyplot(fig)

    # ========== RADAR CHART ==========
    st.write("### 🌦️ Climate Condition Overview")
    categories = ["Soil Moisture", "Temperature", "Humidity"]
    values = [Soil_Moisture, Temperature, Humidity]
    values += values[:1]
    angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(4,4), subplot_kw=dict(polar=True))  # ✅ smaller radar
    ax.fill(angles, values, color="green", alpha=0.25)
    ax.plot(angles, values, color="green", linewidth=2)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_yticklabels([])
    ax.set_title("Climate Conditions", size=14, color="darkgreen")
    st.pyplot(fig)

    st.write("---")
    st.info("💡 Tip: Balanced soil nutrients, proper irrigation & smart fertilizer use = higher yield!")

# Footer
st.markdown(
    "<p style='text-align:center; color:gray;'>🚀 Built with Streamlit | Powered by AI</p>",
    unsafe_allow_html=True
)
