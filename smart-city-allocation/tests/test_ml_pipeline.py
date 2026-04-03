#!/usr/bin/env python3
"""
Test ML Pipeline
Tests that models load correctly, return valid predictions, and feature lists match.
"""
import os
import sys
import pytest
import joblib
import pandas as pd
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.models.ml_constants import TRAFFIC_FEATURES, WASTE_FEATURES, EMERGENCY_FEATURES
from api.models.schemas import TrafficPredictionRequest, WastePredictionRequest
from api.services.ml_service import predict_traffic, predict_waste, load_models


class TestTrafficModel:
    """Test traffic model loading and predictions"""
    
    @classmethod
    def setup_class(cls):
        """Load models before tests"""
        load_models()
    
    def test_traffic_model_loads(self):
        """Test 1: Traffic model loads successfully"""
        model_path = "traffic_model.pkl"
        assert os.path.exists(model_path), "Traffic model file not found"
        
        model = joblib.load(model_path)
        assert model is not None, "Traffic model failed to load"
        assert hasattr(model, 'predict'), "Model doesn't have predict method"
        assert hasattr(model, 'predict_proba'), "Model doesn't have predict_proba method"
    
    def test_traffic_prediction_returns_valid_probability(self):
        """Test 2: Traffic prediction returns probability between 0 and 1"""
        req = TrafficPredictionRequest(
            hour=8,
            day_enc=1,
            junction_enc=0,
            weather_enc=0,
            temperature_c=25.0,
            vehicles=300
        )
        
        result = predict_traffic(req)
        
        assert result is not None, "Prediction returned None"
        assert hasattr(result, 'numeric_score'), "Result missing numeric_score"
        assert 0 <= result.numeric_score <= 1, f"Probability {result.numeric_score} not in [0,1]"
        assert result.congestion_level in ['low', 'high'], "Invalid congestion level"
    
    def test_traffic_features_match_model(self):
        """Test 3: TRAFFIC_FEATURES matches what the model expects"""
        model = joblib.load("traffic_model.pkl")
        
        # Get expected features from model
        if hasattr(model, "named_steps"):
            first_step = list(model.named_steps.values())[0]
            if hasattr(first_step, "feature_names_in_"):
                model_features = list(first_step.feature_names_in_)
                
                assert len(TRAFFIC_FEATURES) == len(model_features), \
                    f"Feature count mismatch: {len(TRAFFIC_FEATURES)} vs {len(model_features)}"
                
                assert TRAFFIC_FEATURES == model_features, \
                    f"Feature mismatch:\n  Constants: {TRAFFIC_FEATURES}\n  Model: {model_features}"
    
    def test_traffic_prediction_with_edge_cases(self):
        """Test 4: Traffic prediction handles edge cases"""
        # Test with minimum values
        req_min = TrafficPredictionRequest(
            hour=0, day_enc=0, junction_enc=0, weather_enc=0,
            temperature_c=18.0, vehicles=20
        )
        result_min = predict_traffic(req_min)
        assert 0 <= result_min.numeric_score <= 1
        
        # Test with maximum values
        req_max = TrafficPredictionRequest(
            hour=23, day_enc=6, junction_enc=7, weather_enc=3,
            temperature_c=42.0, vehicles=600
        )
        result_max = predict_traffic(req_max)
        assert 0 <= result_max.numeric_score <= 1


class TestWasteModel:
    """Test waste model loading and predictions"""
    
    @classmethod
    def setup_class(cls):
        """Load models before tests"""
        load_models()
    
    def test_waste_model_loads(self):
        """Test 5: Waste model loads successfully"""
        model_path = "waste_model.pkl"
        assert os.path.exists(model_path), "Waste model file not found"
        
        model = joblib.load(model_path)
        assert model is not None, "Waste model failed to load"
        assert hasattr(model, 'predict'), "Model doesn't have predict method"
    
    def test_waste_prediction_returns_valid_probability(self):
        """Test 6: Waste prediction returns probability between 0 and 1"""
        req = WastePredictionRequest(
            area=0,
            day_of_week=4,
            population_density=2.0,
            last_collection_days=5,
            bin_fill_pct=85.0
        )
        
        result = predict_waste(req)
        
        assert result is not None, "Prediction returned None"
        assert hasattr(result, 'numeric_score'), "Result missing numeric_score"
        assert 0 <= result.numeric_score <= 1, f"Probability {result.numeric_score} not in [0,1]"
        assert result.overflow_risk in ['low', 'high'], "Invalid overflow risk"
    
    def test_waste_features_match_model(self):
        """Test 7: WASTE_FEATURES matches what the model expects"""
        model = joblib.load("waste_model.pkl")
        
        # Get expected features from model
        if hasattr(model, "named_steps"):
            first_step = list(model.named_steps.values())[0]
            if hasattr(first_step, "feature_names_in_"):
                model_features = list(first_step.feature_names_in_)
                
                assert len(WASTE_FEATURES) == len(model_features), \
                    f"Feature count mismatch: {len(WASTE_FEATURES)} vs {len(model_features)}"
                
                assert WASTE_FEATURES == model_features, \
                    f"Feature mismatch:\n  Constants: {WASTE_FEATURES}\n  Model: {model_features}"


class TestEmergencyModel:
    """Test emergency model loading"""
    
    def test_emergency_model_loads(self):
        """Test 8: Emergency model loads successfully"""
        model_path = "emergency_model.pkl"
        assert os.path.exists(model_path), "Emergency model file not found"
        
        model = joblib.load(model_path)
        assert model is not None, "Emergency model failed to load"
        assert hasattr(model, 'predict'), "Model doesn't have predict method"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
