def calculate_roi(traffic_level: float, waste_level: float):
    """
    Simulates the financial impact of the AI decision platform by calculating
    baseline costs vs AI optimized costs for resource allocation.
    """
    # Assumptions for a city (e.g., Udaipur)
    
    # Baseline manual system
    # Daily waste patrols: constant 50 runs/day
    base_waste_cost = 50 * 500  # Rs. 500 per run
    
    # Baseline traffic congestion delay economic cost (assumed high if unused)
    # Using a flat high congestion metric for unoptimized
    base_traffic_cost = 15000 
    
    baseline_daily_cost = base_waste_cost + base_traffic_cost
    
    # AI Optimized system
    # Waste runs strictly based on 'High' or 'Overflow' risk
    ai_waste_runs = 20 if waste_level > 0.70 else 5  # targeted only
    ai_waste_cost = ai_waste_runs * 500
    
    # AI traffic delay cost (reduced heavily by AI routing/signals)
    # Reduced by a factor as AI actively mitigates high traffic
    ai_traffic_cost = (traffic_level) * 10000 
    
    ai_daily_cost = ai_waste_cost + ai_traffic_cost
    
    daily_savings = baseline_daily_cost - ai_daily_cost
    monthly_savings = daily_savings * 30
    
    efficiency_gain = (daily_savings / baseline_daily_cost) * 100 if baseline_daily_cost > 0 else 0
    
    return {
        "monthly_savings": int(monthly_savings),
        "efficiency_gain": round(efficiency_gain, 1),
        "baseline_cost": int(baseline_daily_cost * 30),
        "ai_cost": int(ai_daily_cost * 30)
    }
