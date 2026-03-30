# Baseline assumptions (rupees)
TRUCK_DEPLOYMENT_COST = 500  # Per waste collection truck run
EMERGENCY_COLLECTION_COST = 800  # Premium cost for overflow emergency runs
POLICE_PER_HOUR_COST = 200  # Manual traffic control overhead
AMBULANCE_DISPATCH_COST = 2000  # Cost per emergency dispatch

def calculate_baseline_cost() -> int:
    """
    Fixed/manual operations baseline.
    Assumes fixed daily patrols and unoptimized operations across the city.
    """
    # 10 waste patrols a day
    waste_cost = 10 * TRUCK_DEPLOYMENT_COST
    # Fixed traffic police deployment (e.g., 20 hours a day across junctions)
    traffic_cost = 20 * POLICE_PER_HOUR_COST
    # Fixed 5 emergency dispatches
    emergency_cost = 5 * AMBULANCE_DISPATCH_COST
    
    daily_cost = waste_cost + traffic_cost + emergency_cost
    monthly_baseline = daily_cost * 30
    return int(monthly_baseline)

def calculate_optimized_cost(traffic_level: float, waste_level: float, emergencies_count: int) -> int:
    """
    AI Optimized Cost based on targeted deployment.
    """
    # Waste: only deploy where needed, but add emergency premium if overflow
    if waste_level > 0.90:
        waste_cost = 2 * EMERGENCY_COLLECTION_COST  # emergency immediate dispatches
    elif waste_level > 0.70:
        waste_cost = 4 * TRUCK_DEPLOYMENT_COST  # targeted collections
    else:
        waste_cost = 1 * TRUCK_DEPLOYMENT_COST  # minimal routine checks
        
    # Traffic: reduced delay / police deployment based on AI signal optimizations
    if traffic_level > 0.60:
        traffic_cost = int(traffic_level * 10 * POLICE_PER_HOUR_COST)
    else:
        traffic_cost = 0
    
    # Emergency: Optimized routes / accurate dispatching
    emergency_cost = emergencies_count * AMBULANCE_DISPATCH_COST
    
    daily_cost = waste_cost + traffic_cost + emergency_cost
    monthly_optimized = daily_cost * 30
    return int(monthly_optimized)
