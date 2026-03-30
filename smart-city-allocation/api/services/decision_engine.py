from api.models.schemas import (
    DecisionResponse, DecisionTraffic, DecisionWaste, DecisionEmergency, AlertLevel,
    TrafficPredictionRequest, WastePredictionRequest
)
from api.services.simulation_service import get_current_state
from api.services.alert_service import evaluate_alerts
from api.services.ml_service import get_traffic_explanation, get_waste_explanation
from api.services.cost_analysis_service import calculate_costs
from api.services.history_service import append_history
import datetime

def calculate_city_health_score(max_traffic: float, max_waste: float, emergencies: list, alerts: list) -> float:
    score = 100.0
    score -= min(35, max_traffic * 0.35)
    score -= min(30, max_waste * 0.30)
    score -= min(20, len(emergencies) * 5)
    score -= min(15, len(alerts) * 1.5)
    return round(max(0, score), 1)

def predict_overflow_eta(current_fill: float) -> str:
    avg_fill_rate_per_minute = 0.36
    if current_fill >= 100:
        return "OVERFLOW NOW"
    if current_fill < 50:
        return "Safe"
    minutes_left = (100 - current_fill) / avg_fill_rate_per_minute
    if minutes_left < 60:
        return f"~{int(minutes_left)} min"
    return f"~{minutes_left/60:.1f} hrs"

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
        
    # Generate ML Explainability for the worst cases
    now = datetime.datetime.now()
    t_req = TrafficPredictionRequest(
        hour=now.hour,
        day_enc=now.weekday(),
        junction_enc=1,
        weather_enc=state.get("weather_enc", 0),
        vehicles=int((max_traffic / 100) * 800)
    )
    t_pred = 1 if max_traffic >= 60 else 0
    t_exp = get_traffic_explanation(t_req, max_traffic / 100, t_pred)

    w_req = WastePredictionRequest(
        area=1,
        day_of_week=now.weekday(),
        population_density=3500.0,
        last_collection_days=3,
        bin_fill_pct=max_waste / 100
    )
    w_pred = 1 if max_waste >= 70 else 0
    w_exp = get_waste_explanation(w_req, max_waste / 100, w_pred)

    # Generate ROI Data
    emergencies_count = len(state.get("emergencies", []))
    roi_data = calculate_costs(max_traffic / 100, max_waste / 100, emergencies_count)
    
    # Calculate Phase 2 Metrics
    city_health_score = calculate_city_health_score(max_traffic, max_waste, emergencies, raw_alerts)
    waste_overflow_eta = predict_overflow_eta(max_waste)
    
    # Store metrics for historical trends chart
    append_history(round(max_traffic, 1), round(max_waste, 1))

    return DecisionResponse(
        traffic=DecisionTraffic(value=round(max_traffic, 1), status=t_status, explainability=t_exp, features=t_req),
        waste=DecisionWaste(value=round(max_waste, 1), risk=w_risk, explainability=w_exp, features=w_req, waste_overflow_eta=waste_overflow_eta),
        emergency=DecisionEmergency(type=e_type, severity=e_sev),
        alerts=alerts,
        actions=actions,
        data_source=state.get("data_source", "simulated"),
        roi=roi_data,
        city_health_score=city_health_score
    )
