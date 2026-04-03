#!/usr/bin/env python3
"""Quick script to retrain traffic model with corrected 6 features (including temperature_c)"""
import os
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Load data
data_path = "data/traffic_clean.csv"
df = pd.read_csv(data_path)

print(f"Loaded {len(df)} rows from {data_path}")
print(f"Columns: {list(df.columns)}")

# Rename columns to match API naming
df = df.rename(columns={
    "junction": "junction_enc",
    "day_of_week": "day_enc",
    "weather": "weather_enc"
})

# Select 6 features (INCLUDING temperature_c)
TRAFFIC_FEATURES = ["hour", "day_enc", "junction_enc", "weather_enc", "temperature_c", "vehicles"]
X = df[TRAFFIC_FEATURES]
y = df["high_congestion"]

print(f"\nFeatures used: {TRAFFIC_FEATURES}")
print(f"Feature shape: {X.shape}")
print(f"Target distribution: {y.value_counts().to_dict()}")

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\nTrain size: {len(X_train)}, Test size: {len(X_test)}")

# Create pipeline
pipeline = Pipeline([
    ("prep", StandardScaler()),
    ("clf", RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        class_weight="balanced"
    ))
])

print("\nTraining model...")
pipeline.fit(X_train, y_train)

# Evaluate
train_score = pipeline.score(X_train, y_train)
test_score = pipeline.score(X_test, y_test)

print(f"Train accuracy: {train_score:.3f}")
print(f"Test accuracy: {test_score:.3f}")

# Save model
model_path = "traffic_model.pkl"
joblib.dump(pipeline, model_path)
print(f"\n✅ Model saved to {model_path}")
print(f"Model expects {len(TRAFFIC_FEATURES)} features: {TRAFFIC_FEATURES}")
