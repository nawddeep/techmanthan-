from typing import Dict, Any
from api.services.cost_calculator import calculate_baseline_cost, calculate_optimized_cost

def calculate_costs(traffic_level: float, waste_level: float, emergencies_count: int) -> Dict[str, Any]:
    """
    Calculate and format the precise ROI fields required for the Decision Engine.
    """
    baseline_cost = calculate_baseline_cost()
    optimized_cost = calculate_optimized_cost(traffic_level, waste_level, emergencies_count)
    
    monthly_savings = baseline_cost - optimized_cost
    
    if baseline_cost > 0:
        savings_percentage = round((monthly_savings / baseline_cost) * 100.0, 1)
    else:
        savings_percentage = 0.0
        
    annual_projection = monthly_savings * 12
    
    return {
        "baseline_cost": int(baseline_cost),
        "optimized_cost": int(optimized_cost),
        "monthly_savings": int(monthly_savings),
        "savings_percentage": float(savings_percentage),
        "annual_projection": int(annual_projection),
        "explanation": "AI reduces unnecessary deployments and optimizes resource usage, leading to cost savings."
    }
