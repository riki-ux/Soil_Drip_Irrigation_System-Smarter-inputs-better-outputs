import joblib

# Load trained model
model = joblib.load("fertilizer_model.pkl")

# Example input: [Soil_Moisture, N, P, K, Temperature, Humidity]
sample = [[35, 15, 40, 60, 28.5, 65]]

# Predict
prediction = model.predict(sample)

print("🌱 Fertilizer Needed?" , "Yes" if prediction[0] == 1 else "No")
