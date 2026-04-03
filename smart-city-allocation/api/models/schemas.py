from pydantic import BaseModel
from enum import Enum
from typing import List, Optional
from datetime import datetime

class AlertLevel(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

class EmergencySeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class EventType(str, Enum):
    ACCIDENT = "accident"
    FIRE = "fire"
    MEDICAL = "medical"

class TrafficPredictionRequest(BaseModel):
    hour: int
    day_enc: int
    junction_enc: int
    weather_enc: int
    temperature_c: float = 25.0  # Default temperature
    vehicles: int

class WastePredictionRequest(BaseModel):
    area: int
    day_of_week: int
    population_density: float
    last_collection_days: int
    bin_fill_pct: float

class TrafficPredictionResponse(BaseModel):
    congestion_level: str
    numeric_score: float
    suggested_action: str

class WastePredictionResponse(BaseModel):
    overflow_risk: str
    priority_level: str
    numeric_score: float
    optimized_collection_suggestion: str

class EmergencyEvent(BaseModel):
    event_type: EventType
    severity: EmergencySeverity
    nearest_response_unit: str
    timestamp: datetime
    location_id: int

class Alert(BaseModel):
    alert_type: AlertLevel
    message: str
    timestamp: datetime
    location_id: Optional[int] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class FeatureDetail(BaseModel):
    feature: str
    display_name: str
    value: float
    impact: float
    effect: str

class ExplainResponse(BaseModel):
    prediction: str
    confidence: float
    top_features: List[FeatureDetail]
    explanation: str

# For backward compatibility with ml_service.py if it's still being used
class ModelExplainability(BaseModel):
    prediction: str
    confidence: float
    top_features: List[FeatureDetail]
    explanation: str

class ROIData(BaseModel):
    baseline_cost: int
    optimized_cost: int
    monthly_savings: int
    savings_percentage: float
    annual_projection: int
    explanation: str

class DecisionTraffic(BaseModel):
    value: float
    status: str
    features: Optional[TrafficPredictionRequest] = None
    explainability: Optional[ModelExplainability] = None

class DecisionWaste(BaseModel):
    value: float
    risk: str
    features: Optional[WastePredictionRequest] = None
    explainability: Optional[ModelExplainability] = None
    waste_overflow_eta: str = "N/A"

class DecisionEmergency(BaseModel):
    type: str
    severity: str
    worst_zone_id: Optional[int] = None
    worst_zone_risk_score: Optional[float] = None
    explainability: Optional[ModelExplainability] = None


class DecisionResponse(BaseModel):
    traffic: DecisionTraffic
    waste: DecisionWaste
    emergency: DecisionEmergency
    alerts: List[str]
    actions: List[str]
    data_source: str = "simulated"
    roi: ROIData
    city_health_score: float = 100.0


class MapDataLocation(BaseModel):
    location_id: int
    coordinates: List[float]
    traffic_intensity: str
    waste_status: str
    alerts_count: int
    junction_name: Optional[str] = None
    traffic_ml_label: Optional[str] = None
    traffic_ml_probability: Optional[float] = None
    waste_ml_label: Optional[str] = None
    waste_ml_probability: Optional[float] = None
    emergency_risk_score: Optional[float] = None
