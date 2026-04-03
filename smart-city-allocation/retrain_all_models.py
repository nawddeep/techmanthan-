#!/usr/bin/env python3
"""
Retrain all three models (traffic, waste, emergency) with the new realistic data.
This ensures predictions are consistent with the simulation.
"""
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

print("="*60)
print("Retraining All Models with Realistic Data")
print("="*60)

# ============================================================================
# 1. TRAFFIC MODEL
# ============================================================================
print("\n[1/3] Training Traffic Model...")
traffic_df = pd.read_csv("data/traffic_clean.csv")

# Rename columns to match API
traffic_df = traffic_df.rename(columns={
    "junction": "junction_enc",
    "day_of_week": "day_enc",
    "weather": "weather_enc"
})

# Features (6 features including temperature_c)
TRAFFIC_FEATURES = ["hour", "day_enc", "junction_enc", "weather_enc", "temperature_c", "vehicles"]
X_traffic = traffic_df[TRAFFIC_FEATURES]
y_traffic = traffic_df["high_congestion"]

print(f"  Data: {len(X_traffic)} samples, {X_traffic.shape[1]} features")
print(f"  Target distribution: {y_traffic.value_counts().to_dict()}")

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X_traffic, y_traffic, test_size=0.2, random_state=42, stratify=y_traffic
)

# Train pipeline
traffic_pipeline = Pipeline([
    ("prep", StandardScaler()),
    ("clf", RandomForestClassifier(
        n_estimators=100,
        max_depth=12,
        min_samples_split=5,
        random_state=42,
        class_weight="balanced"
    ))
])

traffic_pipeline.fit(X_train, y_train)

# Evaluate
y_pred = traffic_pipeline.predict(X_test)
acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred, zero_division=0)
rec = recall_score(y_test, y_pred, zero_division=0)
f1 = f1_score(y_test, y_pred, zero_division=0)

print(f"  Accuracy: {acc:.3f}")
print(f"  Precision: {prec:.3f}, Recall: {rec:.3f}, F1: {f1:.3f}")

# Save
joblib.dump(traffic_pipeline, "traffic_model.pkl")
print(f"  ✅ Saved: traffic_model.pkl")

# ============================================================================
# 2. WASTE MODEL
# ============================================================================
print("\n[2/3] Training Waste Model...")
waste_df = pd.read_csv("data/waste_clean.csv")

# Features
WASTE_FEATURES = ["area", "day_of_week", "population_density", "last_collection_days", "bin_fill_pct"]
X_waste = waste_df[WASTE_FEATURES]
y_waste = waste_df["overflow_risk"]

print(f"  Data: {len(X_waste)} samples, {X_waste.shape[1]} features")
print(f"  Target distribution: {y_waste.value_counts().to_dict()}")

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X_waste, y_waste, test_size=0.2, random_state=42, stratify=y_waste
)

# Train pipeline
waste_pipeline = Pipeline([
    ("prep", StandardScaler()),
    ("clf", GradientBoostingClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=42
    ))
])

waste_pipeline.fit(X_train, y_train)

# Evaluate
y_pred = waste_pipeline.predict(X_test)
acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred, zero_division=0)
rec = recall_score(y_test, y_pred, zero_division=0)
f1 = f1_score(y_test, y_pred, zero_division=0)

print(f"  Accuracy: {acc:.3f}")
print(f"  Precision: {prec:.3f}, Recall: {rec:.3f}, F1: {f1:.3f}")

# Save
joblib.dump(waste_pipeline, "waste_model.pkl")
print(f"  ✅ Saved: waste_model.pkl")

# ============================================================================
# 3. EMERGENCY MODEL
# ============================================================================
print("\n[3/3] Training Emergency Model...")
emergency_df = pd.read_csv("data/emergency_clean.csv")

# Features
EMERGENCY_FEATURES = ["zone", "hour", "day_of_week", "weather", "road_condition"]
X_emergency = emergency_df[EMERGENCY_FEATURES]
y_emergency = emergency_df["high_risk"]

print(f"  Data: {len(X_emergency)} samples, {X_emergency.shape[1]} features")
print(f"  Target distribution: {y_emergency.value_counts().to_dict()}")

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X_emergency, y_emergency, test_size=0.2, random_state=42, stratify=y_emergency
)

# Train pipeline
emergency_pipeline = Pipeline([
    ("prep", StandardScaler()),
    ("clf", GradientBoostingClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1,
        random_state=42
    ))
])

emergency_pipeline.fit(X_train, y_train)

# Evaluate
y_pred = emergency_pipeline.predict(X_test)
acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred, zero_division=0)
rec = recall_score(y_test, y_pred, zero_division=0)
f1 = f1_score(y_test, y_pred, zero_division=0)

print(f"  Accuracy: {acc:.3f}")
print(f"  Precision: {prec:.3f}, Recall: {rec:.3f}, F1: {f1:.3f}")

# Save
joblib.dump(emergency_pipeline, "emergency_model.pkl")
print(f"  ✅ Saved: emergency_model.pkl")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*60)
print("Model Retraining Complete!")
print("="*60)
print("\n✅ All models trained with realistic Udaipur data")
print("✅ Traffic: Rush hour patterns (8-10am, 5-7pm)")
print("✅ Waste: Weekly progression (low Monday, high Friday)")
print("✅ Emergency: Rare events (3-5% high-risk)")
print("\nModels saved:")
print("  - traffic_model.pkl")
print("  - waste_model.pkl")
print("  - emergency_model.pkl")
print("\nNext: Restart API server to load new models")
print("  uvicorn api.main:app --reload --host 0.0.0.0 --port 8000")
print("="*60)
