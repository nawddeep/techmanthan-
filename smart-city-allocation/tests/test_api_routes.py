#!/usr/bin/env python3
"""
Test API Routes
Tests that key API endpoints return 200 and valid responses.
"""
import os
import sys
import pytest
import requests
import time

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_URL = "http://127.0.0.1:8000"


class TestAPIRoutes:
    """Test API endpoint availability and responses"""
    
    @classmethod
    def setup_class(cls):
        """Wait for server to be ready"""
        max_retries = 5
        for i in range(max_retries):
            try:
                response = requests.get(f"{BASE_URL}/health", timeout=2)
                if response.status_code == 200:
                    break
            except:
                if i < max_retries - 1:
                    time.sleep(1)
                else:
                    pytest.skip("API server not running")
    
    def test_health_endpoint_returns_200(self):
        """Test 9: /health endpoint returns 200"""
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        assert response.status_code == 200, f"Health endpoint returned {response.status_code}"
    
    def test_health_endpoint_returns_valid_json(self):
        """Test 10: /health returns valid JSON with expected fields"""
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        data = response.json()
        
        assert "status" in data, "Health response missing 'status'"
        assert data["status"] == "healthy", f"Status is {data['status']}, expected 'healthy'"
        assert "models_loaded" in data, "Health response missing 'models_loaded'"
        assert "traffic" in data["models_loaded"], "Missing traffic model status"
        assert "waste" in data["models_loaded"], "Missing waste model status"
        assert "emergency" in data["models_loaded"], "Missing emergency model status"
    
    def test_system_decision_endpoint_returns_200(self):
        """Test 11: /system/decision endpoint returns 200"""
        response = requests.get(f"{BASE_URL}/system/decision", timeout=5)
        assert response.status_code == 200, f"Decision endpoint returned {response.status_code}"
    
    def test_system_decision_returns_valid_structure(self):
        """Test 12: /system/decision returns valid decision structure"""
        response = requests.get(f"{BASE_URL}/system/decision", timeout=5)
        data = response.json()
        
        # Check required top-level fields
        required_fields = ["traffic", "waste", "emergency", "actions", "city_health_score"]
        for field in required_fields:
            assert field in data, f"Decision response missing '{field}'"
        
        # Check traffic structure
        assert "value" in data["traffic"], "Traffic missing 'value'"
        assert "status" in data["traffic"], "Traffic missing 'status'"
        
        # Check waste structure
        assert "value" in data["waste"], "Waste missing 'value'"
        assert "risk" in data["waste"], "Waste missing 'risk'"
        
        # Check actions is a list
        assert isinstance(data["actions"], list), "Actions should be a list"
        
        # Check city health score is a number
        assert isinstance(data["city_health_score"], (int, float)), "City health score should be numeric"
    
    def test_map_data_endpoint_returns_200(self):
        """Test 13: /map-data endpoint returns 200"""
        # Get auth token first
        login_data = {"username": "admin", "password": "admin123"}
        token_response = requests.post(
            f"{BASE_URL}/auth/token",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=5
        )
        
        if token_response.status_code == 200:
            token = token_response.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(f"{BASE_URL}/map-data", headers=headers, timeout=5)
        else:
            # Try without auth (might be public)
            response = requests.get(f"{BASE_URL}/map-data", timeout=5)
        
        assert response.status_code == 200, f"Map-data endpoint returned {response.status_code}"
    
    def test_map_data_returns_10_locations(self):
        """Test 14: /map-data returns 10 locations"""
        # Get auth token first
        login_data = {"username": "admin", "password": "admin123"}
        token_response = requests.post(
            f"{BASE_URL}/auth/token",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=5
        )
        
        if token_response.status_code == 200:
            token = token_response.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(f"{BASE_URL}/map-data", headers=headers, timeout=5)
        else:
            response = requests.get(f"{BASE_URL}/map-data", timeout=5)
        
        data = response.json()
        assert isinstance(data, list), "Map-data should return a list"
        assert len(data) == 10, f"Expected 10 locations, got {len(data)}"
        
        # Check first location has required fields
        if len(data) > 0:
            loc = data[0]
            assert "location_id" in loc, "Location missing 'location_id'"
            assert "coordinates" in loc, "Location missing 'coordinates'"
            assert "traffic_intensity" in loc, "Location missing 'traffic_intensity'"
            assert "waste_status" in loc, "Location missing 'waste_status'"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
