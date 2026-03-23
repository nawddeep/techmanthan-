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

class MapDataLocation(BaseModel):
    location_id: int
    coordinates: List[float]
    traffic_intensity: str
    waste_status: str
    alerts_count: int

class Token(BaseModel):
    access_token: str
    token_type: str

class DecisionTraffic(BaseModel):
    value: float
    status: str

class DecisionWaste(BaseModel):
    value: float
    risk: str

class DecisionEmergency(BaseModel):
    type: str
    severity: str

class DecisionResponse(BaseModel):
    traffic: DecisionTraffic
    waste: DecisionWaste
    emergency: DecisionEmergency
    alerts: List[str]
    actions: List[str]
