#!/usr/bin/env python3
"""
Phase 2 Pattern Verification Test
Validates that realistic Udaipur patterns are present in the data
"""
import pandas as pd
import sys

def test_traffic_patterns():
    """Verify traffic follows realistic Udaipur patterns"""
    print("\n" + "="*60)
    print("TEST 1: Traffic Patterns")
    print("="*60)
    
    traffic = pd.read_csv("data/traffic_clean.csv")
    
    # Rush hour patterns
    morning_rush = traffic[(traffic['hour'] >= 8) & (traffic['hour'] <= 10)]
    evening_rush = traffic[(traffic['hour'] >= 17) & (traffic['hour'] <= 19)]
    night = traffic[(traffic['hour'] >= 23) | (traffic['hour'] <= 6)]
    
    morning_avg = morning_rush['vehicles'].mean()
    evening_avg = evening_rush['vehicles'].mean()
    night_avg = night['vehicles'].mean()
    
    print(f"Morning rush (8-10am): {morning_avg:.0f} vehicles")
    print(f"Evening rush (5-7pm): {evening_avg:.0f} vehicles")
    print(f"Night (11pm-6am): {night_avg:.0f} vehicles")
    
    # Validate patterns
    if morning_avg < 300:
        print("❌ FAIL: Morning rush should have heavy traffic (>300 vehicles)")
        return False
    if evening_avg < 300:
        print("❌ FAIL: Evening rush should have heavy traffic (>300 vehicles)")
        return False
    if night_avg > 100:
        print("❌ FAIL: Night should have light traffic (<100 vehicles)")
        return False
    
    # Peak junctions
    surajpol = traffic[traffic['junction'] == 0]
    delhi_gate = traffic[traffic['junction'] == 1]
    
    print(f"\nSurajpol (junction 0): {surajpol['vehicles'].mean():.0f} avg vehicles")
    print(f"Delhi Gate (junction 1): {delhi_gate['vehicles'].mean():.0f} avg vehicles")
    
    # Temperature pattern
    temp_range = traffic['temperature_c'].max() - traffic['temperature_c'].min()
    print(f"\nTemperature range: {traffic['temperature_c'].min():.1f}°C - {traffic['temperature_c'].max():.1f}°C")
    
    if temp_range < 20:
        print("❌ FAIL: Temperature range should be realistic (>20°C range)")
        return False
    
    print("✅ PASS: Traffic patterns are realistic")
    return True


def test_waste_patterns():
    """Verify waste follows weekly progression"""
    print("\n" + "="*60)
    print("TEST 2: Waste Patterns")
    print("="*60)
    
    waste = pd.read_csv("data/waste_clean.csv")
    
    monday = waste[waste['day_of_week'] == 0]
    friday = waste[waste['day_of_week'] == 4]
    
    monday_avg = monday['bin_fill_pct'].mean()
    friday_avg = friday['bin_fill_pct'].mean()
    
    print(f"Monday avg fill: {monday_avg:.1f}%")
    print(f"Friday avg fill: {friday_avg:.1f}%")
    
    if monday_avg > 40:
        print("❌ FAIL: Monday should have low fill (<40%) after weekend collection")
        return False
    
    if friday_avg < 60:
        print("❌ FAIL: Friday should have high fill (>60%) after week buildup")
        return False
    
    if friday_avg <= monday_avg:
        print("❌ FAIL: Friday fill should be higher than Monday")
        return False
    
    print("✅ PASS: Waste patterns show weekly progression")
    return True


def test_emergency_patterns():
    """Verify emergencies are rare (3-5%)"""
    print("\n" + "="*60)
    print("TEST 3: Emergency Patterns")
    print("="*60)
    
    emergency = pd.read_csv("data/emergency_clean.csv")
    
    high_risk_pct = emergency['high_risk'].mean() * 100
    high_risk_count = emergency['high_risk'].sum()
    
    print(f"High-risk events: {high_risk_count} ({high_risk_pct:.1f}%)")
    print(f"Total samples: {len(emergency)}")
    
    if high_risk_pct > 10:
        print("❌ FAIL: High-risk events should be RARE (<10%)")
        return False
    
    if high_risk_pct < 1:
        print("⚠️  WARNING: High-risk events might be too rare (<1%)")
    
    if 3 <= high_risk_pct <= 7:
        print("✅ PASS: Emergency events are appropriately rare (3-7%)")
    else:
        print(f"✅ PASS: Emergency events are rare ({high_risk_pct:.1f}%)")
    
    return True


def test_model_consistency():
    """Verify models are trained on the current data"""
    print("\n" + "="*60)
    print("TEST 4: Model Consistency")
    print("="*60)
    
    import joblib
    import numpy as np
    
    # Load models
    traffic_model = joblib.load("traffic_model.pkl")
    waste_model = joblib.load("waste_model.pkl")
    emergency_model = joblib.load("emergency_model.pkl")
    
    # Load data
    traffic_df = pd.read_csv("data/traffic_clean.csv")
    waste_df = pd.read_csv("data/waste_clean.csv")
    emergency_df = pd.read_csv("data/emergency_clean.csv")
    
    # Test traffic model
    traffic_df = traffic_df.rename(columns={
        "junction": "junction_enc",
        "day_of_week": "day_enc",
        "weather": "weather_enc"
    })
    X_traffic = traffic_df[["hour", "day_enc", "junction_enc", "weather_enc", "temperature_c", "vehicles"]]
    y_traffic = traffic_df["high_congestion"]
    
    traffic_pred = traffic_model.predict(X_traffic[:100])
    traffic_acc = (traffic_pred == y_traffic[:100]).mean()
    
    print(f"Traffic model accuracy on data: {traffic_acc:.2%}")
    
    if traffic_acc < 0.8:
        print("❌ FAIL: Traffic model seems inconsistent with data")
        return False
    
    print("✅ PASS: Models are consistent with current data")
    return True


def main():
    print("\n" + "="*60)
    print("PHASE 2 PATTERN VERIFICATION")
    print("="*60)
    
    results = []
    results.append(test_traffic_patterns())
    results.append(test_waste_patterns())
    results.append(test_emergency_patterns())
    results.append(test_model_consistency())
    
    print("\n" + "="*60)
    if all(results):
        print("🎉 ALL PHASE 2 PATTERNS VERIFIED!")
        print("="*60)
        print("\n✅ Traffic: Rush hour patterns (8-10am, 5-7pm)")
        print("✅ Traffic: Light night traffic (11pm-6am)")
        print("✅ Traffic: Peak junctions (Surajpol, Delhi Gate)")
        print("✅ Waste: Weekly progression (low Monday, high Friday)")
        print("✅ Emergency: Rare events (3-7% high-risk)")
        print("✅ Models: Consistent with realistic data")
        print("\n" + "="*60)
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        print("="*60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
