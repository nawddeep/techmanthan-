import requests
import json
import sys
from api.models.schemas import DecisionResponse
from pydantic import ValidationError

def test_system_decision():
    print("Running Phase 1 Validation Suite...")
    url = "http://127.0.0.1:8000/system/decision"
    
    try:
        response = requests.get(url, timeout=5)
    except Exception as e:
        print(f"FAILED: Could not connect to {url}. Error: {e}")
        sys.exit(1)
        
    print(f"1. HTTP Status Code: {response.status_code}")
    if response.status_code != 200:
        print("FAILED: Did not return 200 OK.")
        print(response.text)
        sys.exit(1)
        
    data = response.json()
    
    print("2. Validating JSON payload against Pydantic DecisionResponse schema...")
    try:
        # If schema matches, this will succeed
        model = DecisionResponse(**data)
        print("SUCCESS: JSON structure perfectly matches Pydantic schema. No Missing Fields.")
    except ValidationError as e:
        print("FAILED: Schema Mismatch!")
        print(e)
        sys.exit(1)
        
    print("3. Checking for specific strictly added explainability keys...")
    traffic_explain = data.get("traffic", {}).get("explainability", None)
    waste_explain = data.get("waste", {}).get("explainability", None)
    
    if traffic_explain:
        print(f"SUCCESS: Traffic explainability object is present: {list(traffic_explain.keys())}")
    else:
        print("FAILED: Traffic explainability missing.")
        sys.exit(1)
        
    if waste_explain:
        print(f"SUCCESS: Waste explainability object is present: {list(waste_explain.keys())}")
    else:
        print("FAILED: Waste explainability missing.")
        sys.exit(1)
        
    print("\nALL PHASE 1 TESTS PASSED PERFECTLY!")

if __name__ == "__main__":
    test_system_decision()
