from api.models.schemas import DecisionResponse, DecisionTraffic, DecisionWaste, DecisionEmergency, AlertLevel
from api.services.simulation_service import get_current_state
from api.services.alert_service import evaluate_alerts

def generate_decisions() -> DecisionResponse:
    state = get_current_state()
    raw_alerts = evaluate_alerts()
    
    # Extract string messages for alerts
    alerts = [a.message for a in raw_alerts]
    
    # 1. Aggregate Traffic
    traffic_vals = list(state["traffic_levels"].values())
    max_traffic = max(traffic_vals) * 100 if traffic_vals else 0
    
    if max_traffic > 85:
        t_status = "High"
    elif max_traffic >= 60:
        t_status = "Medium"
    else:
        t_status = "Low"
    
    # 2. Aggregate Waste
    waste_vals = list(state["waste_levels"].values())
    max_waste = max(waste_vals) * 100 if waste_vals else 0
    
    if max_waste > 90:
        w_risk = "Overflow"
    elif max_waste >= 70:
        w_risk = "High"
    else:
        w_risk = "Low"
    
    # 3. Emergency state
    emergencies = state["emergencies"]
    e_type = "None"
    e_sev = "Low"
    for em in emergencies:
        if em.severity == "high" or e_type == "None":
            e_type = em.event_type.value.capitalize()
            e_sev = em.severity.value.capitalize()
            if em.severity == "high":
                break
                
    # 4. Generate Actions using Advanced Logic
    actions = []
    
    # Traffic Logic
    if max_traffic > 85:
        actions.append("Deploy traffic police at heavily congested junctions.")
    elif max_traffic >= 60:
        actions.append("Optimize traffic signals to improve flow.")
        
    # Waste Logic
    if max_waste > 90:
        actions.append("Send immediate waste collection vehicle to critical zones.")
    elif max_waste >= 70:
        actions.append("Schedule waste collection for high-risk areas in next cycle.")
        
    # Emergency Logic
    if e_sev == "High":
        actions.append(f"Dispatch nearest emergency response unit immediately for {e_type}.")
    elif e_sev == "Medium":
        actions.append(f"Monitor {e_type} emergency and prepare response units.")
        
    # Catch-all
    if not actions:
        actions.append("Maintain routine city operations.")
        
    return DecisionResponse(
        traffic=DecisionTraffic(value=round(max_traffic, 1), status=t_status),
        waste=DecisionWaste(value=round(max_waste, 1), risk=w_risk),
        emergency=DecisionEmergency(type=e_type, severity=e_sev),
        alerts=alerts,
        actions=actions
    )
