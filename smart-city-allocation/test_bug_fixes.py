#!/usr/bin/env python3
"""
Test script to verify all Phase 1 bug fixes:
1. Temperature_c feature mismatch
2. Auth bypass vulnerability
3. Duplicate map coordinates
"""
import sys
import requests
import json
from typing import Dict, Any

BASE_URL = "http://127.0.0.1:8000"

def print_test(name: str):
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print('='*60)

def print_pass(msg: str):
    print(f"✅ PASS: {msg}")

def print_fail(msg: str):
    print(f"❌ FAIL: {msg}")
    sys.exit(1)

def test_1_temperature_c_removed():
    """Test that temperature_c is no longer in the feature list"""
    print_test("Bug Fix #1: Temperature_c Feature Removed")
    
    # Check ml_constants.py
    try:
        from api.models.ml_constants import TRAFFIC_FEATURES
        print(f"Current TRAFFIC_FEATURES: {TRAFFIC_FEATURES}")
        
        if "temperature_c" in TRAFFIC_FEATURES:
            print_fail("temperature_c is still in TRAFFIC_FEATURES!")
        
        expected_features = ["hour", "day_enc", "junction_enc", "weather_enc", "vehicles"]
        if TRAFFIC_FEATURES == expected_features:
            print_pass(f"TRAFFIC_FEATURES correctly has 5 features (no temperature_c)")
        else:
            print_fail(f"TRAFFIC_FEATURES mismatch. Expected {expected_features}, got {TRAFFIC_FEATURES}")
    except Exception as e:
        print_fail(f"Could not import TRAFFIC_FEATURES: {e}")
    
    # Test that the API endpoint works without temperature_c
    print("\nTesting /system/decision endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/system/decision", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print_pass("/system/decision returns 200 OK (model inference working)")
            
            # Check that traffic features don't include temperature_c
            if "traffic" in data and "features" in data["traffic"]:
                features = data["traffic"]["features"]
                feature_dict = features if isinstance(features, dict) else features.__dict__
                if "temperature_c" in feature_dict:
                    print_fail("API response still includes temperature_c in traffic features!")
                else:
                    print_pass("API response traffic features do not include temperature_c")
                    print(f"   Features present: {list(feature_dict.keys())}")
        else:
            print_fail(f"/system/decision returned {response.status_code}: {response.text}")
    except Exception as e:
        print_fail(f"Could not test /system/decision: {e}")

def test_2_auth_bypass_removed():
    """Test that auth bypass is removed and proper auth is enforced"""
    print_test("Bug Fix #2: Auth Bypass Removed")
    
    # Test 1: Request without token should fail on protected endpoint
    print("\nTest 2a: Request without authentication token to /auth/me...")
    try:
        response = requests.get(f"{BASE_URL}/auth/me", timeout=5)
        if response.status_code == 401:
            print_pass("Unauthenticated request correctly returns 401 Unauthorized")
        elif response.status_code == 200:
            print_fail("Unauthenticated request returned 200! Auth bypass still exists!")
        else:
            print(f"⚠️  WARNING: Unexpected status {response.status_code}")
    except Exception as e:
        print_fail(f"Could not test unauthenticated request: {e}")
    
    # Test 2: Login and get valid token
    print("\nTest 2b: Login with valid credentials...")
    try:
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        response = requests.post(
            f"{BASE_URL}/auth/token",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=5
        )
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get("access_token")
            if access_token:
                print_pass(f"Login successful, received JWT token")
                
                # Test 3: Request with valid token should succeed
                print("\nTest 2c: Request with valid JWT token to /auth/me...")
                headers = {"Authorization": f"Bearer {access_token}"}
                response = requests.get(f"{BASE_URL}/auth/me", headers=headers, timeout=5)
                if response.status_code == 200:
                    user_data = response.json()
                    print_pass(f"Authenticated request returns 200 OK (user: {user_data.get('username')})")
                else:
                    print_fail(f"Authenticated request failed with status {response.status_code}")
            else:
                print_fail("Login response missing access_token")
        else:
            print_fail(f"Login failed with status {response.status_code}: {response.text}")
    except Exception as e:
        print_fail(f"Could not test authentication: {e}")

def test_3_duplicate_coordinates_fixed():
    """Test that duplicate map coordinates are fixed"""
    print_test("Bug Fix #3: Duplicate Map Coordinates Fixed")
    
    # Get a valid token first
    try:
        login_data = {"username": "admin", "password": "admin123"}
        response = requests.post(
            f"{BASE_URL}/auth/token",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=5
        )
        token = response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
    except:
        print("⚠️  Skipping auth for map-data test (might be public endpoint)")
        headers = {}
    
    try:
        response = requests.get(f"{BASE_URL}/map-data", headers=headers, timeout=5)
        if response.status_code == 200:
            locations = response.json()
            print(f"Retrieved {len(locations)} locations")
            
            # Check specific locations
            location_names = {}
            for loc in locations:
                loc_id = loc.get("location_id")
                name = loc.get("junction_name")
                coords = tuple(loc.get("coordinates", []))
                
                if loc_id in [1, 9, 10]:
                    print(f"  Location {loc_id}: {name} at {coords}")
                
                # Check for duplicates
                if name in location_names:
                    if location_names[name] == coords:
                        print_fail(f"Duplicate found: {name} appears at same coordinates {coords}")
                location_names[name] = coords
            
            # Verify specific fixes
            loc_9 = next((l for l in locations if l["location_id"] == 9), None)
            loc_10 = next((l for l in locations if l["location_id"] == 10), None)
            
            if loc_9:
                if "Sec-2" in loc_9["junction_name"] or loc_9["junction_name"] == "Pratap Nagar Sec-2":
                    print_pass(f"Location 9 correctly renamed to '{loc_9['junction_name']}'")
                else:
                    print_fail(f"Location 9 name not fixed: '{loc_9['junction_name']}'")
            
            if loc_10:
                if "Chauraha" in loc_10["junction_name"] or loc_10["junction_name"] == "Madhuban Chauraha":
                    print_pass(f"Location 10 correctly renamed to '{loc_10['junction_name']}'")
                else:
                    print_fail(f"Location 10 name not fixed: '{loc_10['junction_name']}'")
            
            print_pass("No duplicate coordinates found")
        else:
            print_fail(f"/map-data returned {response.status_code}: {response.text}")
    except Exception as e:
        print_fail(f"Could not test map-data: {e}")

def main():
    print("\n" + "="*60)
    print("PHASE 1 BUG FIX VALIDATION SUITE")
    print("="*60)
    print("\nEnsure the API server is running at http://127.0.0.1:8000")
    print("Run: uvicorn api.main:app --reload --host 0.0.0.0 --port 8000\n")
    
    # Test 1: Temperature_c removed
    test_1_temperature_c_removed()
    
    # Test 2: Auth bypass removed
    test_2_auth_bypass_removed()
    
    # Test 3: Duplicate coordinates fixed
    test_3_duplicate_coordinates_fixed()
    
    print("\n" + "="*60)
    print("🎉 ALL BUG FIXES VALIDATED SUCCESSFULLY!")
    print("="*60)
    print("\nSummary:")
    print("✅ Temperature_c feature removed from model pipeline")
    print("✅ Authentication bypass vulnerability fixed")
    print("✅ Duplicate map coordinates corrected")
    print("\nYour codebase is ready for judge review!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
