from datetime import datetime
from typing import List
from api.models.schemas import Alert, AlertLevel, EmergencySeverity
from api.services.simulation_service import city_state

def evaluate_alerts() -> List[Alert]:
    alerts = []
    for loc, level in city_state["traffic_levels"].items():
        if level > 0.8:
            alerts.append(Alert(
                alert_type=AlertLevel.WARNING,
                message=f"High traffic congestion detected at location {loc} ({level*100:.1f}%)",
                timestamp=datetime.now(),
                location_id=loc
            ))
            
    for loc, level in city_state["waste_levels"].items():
        if level > 0.9:
            alerts.append(Alert(
                alert_type=AlertLevel.CRITICAL,
                message=f"Waste overflow imminent at location {loc} ({level*100:.1f}%)",
                timestamp=datetime.now(),
                location_id=loc
            ))
            
    for em in city_state["emergencies"]:
        alerts.append(Alert(
            alert_type=AlertLevel.CRITICAL
            if em.severity == EmergencySeverity.HIGH
            else AlertLevel.WARNING,
            message=f"{em.event_type.value.capitalize()} emergency reported at location {em.location_id}",
            timestamp=em.timestamp,
            location_id=em.location_id
        ))
        
    return alerts
