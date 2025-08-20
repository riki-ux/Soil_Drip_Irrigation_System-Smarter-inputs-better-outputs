import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# -----------------------------
# Generate Dummy Dataset
# -----------------------------
np.random.seed(42)
n_samples = 200

data = {
    "Soil_Moisture": np.random.randint(10, 100, n_samples),
    "N": np.random.randint(0, 100, n_samples),
    "P": np.random.randint(0, 100, n_samples),
    "K": np.random.randint(0, 100, n_samples),
    "Temperature": np.random.uniform(15, 40, n_samples),
    "Humidity": np.random.uniform(30, 90, n_samples),
}

# Target variable
fertilizer = []
for i in range(n_samples):
    if data["Soil_Moisture"][i] < 40 or data["N"][i] < 20:
        fertilizer.append(1)   # Fertilizer Needed
    else:
        fertilizer.append(0)   # Not Needed

data["Fertilizer_Recommendation"] = fertilizer
df = pd.DataFrame(data)

# -----------------------------
# Train Model
# -----------------------------
X = df.drop("Fertilizer_Recommendation", axis=1)
y = df["Fertilizer_Recommendation"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("✅ Accuracy:", accuracy_score(y_test, y_pred))

# Save model
joblib.dump(model, "fertilizer_model.pkl")
print("💾 Model saved as fertilizer_model.pkl")
