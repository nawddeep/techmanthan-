#!/usr/bin/env python3
"""
Test Decision Engine
Tests the health score formula and decision logic.
"""
import os
import sys
import pytest

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.services.decision_engine import calculate_city_health_score


class TestCityHealthScore:
    """Test city health score calculation"""
    
    def test_clean_city_returns_100(self):
        """Test 15: Clean city (no issues) returns health score of 100"""
        score = calculate_city_health_score(
            max_traffic=0.0,
            max_waste=0.0,
            emergencies=[],
            alerts=[]
        )
        assert score == 100.0, f"Clean city should have score 100, got {score}"
    
    def test_high_traffic_lowers_score(self):
        """Test 16: High traffic (90%) lowers health score"""
        score = calculate_city_health_score(
            max_traffic=90.0,
            max_waste=0.0,
            emergencies=[],
            alerts=[]
        )
        assert score < 100.0, f"High traffic should lower score below 100, got {score}"
        assert score >= 0.0, f"Score should not be negative, got {score}"
        
        # Traffic can deduct up to 35 points
        expected_deduction = min(35, 90.0 * 0.35)
        expected_score = 100.0 - expected_deduction
        assert abs(score - expected_score) < 0.1, \
            f"Expected score ~{expected_score}, got {score}"
    
    def test_high_waste_lowers_score(self):
        """Test 17: High waste (90%) lowers health score"""
        score = calculate_city_health_score(
            max_traffic=0.0,
            max_waste=90.0,
            emergencies=[],
            alerts=[]
        )
        assert score < 100.0, f"High waste should lower score below 100, got {score}"
        assert score >= 0.0, f"Score should not be negative, got {score}"
        
        # Waste can deduct up to 30 points
        expected_deduction = min(30, 90.0 * 0.30)
        expected_score = 100.0 - expected_deduction
        assert abs(score - expected_score) < 0.1, \
            f"Expected score ~{expected_score}, got {score}"
    
    def test_score_never_goes_negative(self):
        """Test 18: Health score never goes negative even with all issues"""
        score = calculate_city_health_score(
            max_traffic=100.0,
            max_waste=100.0,
            emergencies=[1, 2, 3, 4, 5],  # 5 emergencies
            alerts=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # 10 alerts
        )
        assert score >= 0.0, f"Score should never be negative, got {score}"
        assert score <= 100.0, f"Score should never exceed 100, got {score}"
    
    def test_emergencies_lower_score(self):
        """Test 19: Emergencies lower health score"""
        # Create mock emergency objects
        class MockEmergency:
            pass
        
        emergencies = [MockEmergency() for _ in range(3)]
        
        score = calculate_city_health_score(
            max_traffic=0.0,
            max_waste=0.0,
            emergencies=emergencies,
            alerts=[]
        )
        
        # Each emergency deducts 5 points, max 20 points total
        expected_deduction = min(20, len(emergencies) * 5)
        expected_score = 100.0 - expected_deduction
        
        assert score < 100.0, "Emergencies should lower score"
        assert abs(score - expected_score) < 0.1, \
            f"Expected score ~{expected_score}, got {score}"
    
    def test_alerts_lower_score(self):
        """Test 20: System alerts lower health score"""
        # Create mock alert objects
        class MockAlert:
            pass
        
        alerts = [MockAlert() for _ in range(5)]
        
        score = calculate_city_health_score(
            max_traffic=0.0,
            max_waste=0.0,
            emergencies=[],
            alerts=alerts
        )
        
        # Each alert deducts 1.5 points, max 15 points total
        expected_deduction = min(15, len(alerts) * 1.5)
        expected_score = 100.0 - expected_deduction
        
        assert score < 100.0, "Alerts should lower score"
        assert abs(score - expected_score) < 0.1, \
            f"Expected score ~{expected_score}, got {score}"
    
    def test_combined_issues_compound(self):
        """Test 21: Multiple issues compound to lower score"""
        class MockEmergency:
            pass
        class MockAlert:
            pass
        
        score = calculate_city_health_score(
            max_traffic=50.0,
            max_waste=50.0,
            emergencies=[MockEmergency()],
            alerts=[MockAlert(), MockAlert()]
        )
        
        # Calculate expected deductions
        traffic_deduction = min(35, 50.0 * 0.35)  # 17.5
        waste_deduction = min(30, 50.0 * 0.30)    # 15.0
        emergency_deduction = min(20, 1 * 5)       # 5.0
        alert_deduction = min(15, 2 * 1.5)         # 3.0
        
        expected_score = 100.0 - traffic_deduction - waste_deduction - emergency_deduction - alert_deduction
        
        assert abs(score - expected_score) < 0.1, \
            f"Expected score ~{expected_score}, got {score}"
        assert score >= 0.0, "Score should not be negative"
        assert score < 100.0, "Combined issues should lower score"


class TestDecisionLogic:
    """Test decision-making logic"""
    
    def test_health_score_is_rounded(self):
        """Test 22: Health score is rounded to 1 decimal place"""
        score = calculate_city_health_score(
            max_traffic=33.333,
            max_waste=0.0,
            emergencies=[],
            alerts=[]
        )
        
        # Check that score has at most 1 decimal place
        score_str = str(score)
        if '.' in score_str:
            decimals = len(score_str.split('.')[1])
            assert decimals <= 1, f"Score should be rounded to 1 decimal, got {decimals} decimals"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
