import asyncio
import random
from datetime import datetime
from api.models.schemas import EventType, EmergencySeverity, EmergencyEvent
from api.services.external_data_service import get_integrated_data

city_state = {
    "traffic_levels": {loc: random.uniform(0.1, 0.9) for loc in range(1, 11)},
    "waste_levels": {loc: random.uniform(0.1, 0.9) for loc in range(1, 11)},
    "emergencies": [],
    "data_source": "simulated",
    "weather_enc": 0
}

async def run_simulation():
    while True:
        try:
            update_city_state()
        except Exception as e:
            print(f"Simulation error: {e}")
        await asyncio.sleep(5)

def update_city_state():
    # Fetch external data
    ext_data = get_integrated_data()
    city_state["data_source"] = ext_data["source"]
    city_state["weather_enc"] = ext_data["weather_enc"]
    base_traffic = ext_data["base_congestion"]

    for loc in city_state["traffic_levels"]:
        change = random.uniform(-0.15, 0.15)
        # Weight real simulation data in
        new_val = (city_state["traffic_levels"][loc] + change) * 0.5 + (base_traffic * 0.5)
        city_state["traffic_levels"][loc] = max(0.0, min(1.0, new_val))
        
    for loc in city_state["waste_levels"]:
        if random.random() < 0.1:
            city_state["waste_levels"][loc] = random.uniform(0.0, 0.1)
        else:
            city_state["waste_levels"][loc] = min(1.0, city_state["waste_levels"][loc] + random.uniform(0.01, 0.05))
            
    current_time = datetime.now()
    active_emergencies = [em for em in city_state["emergencies"] if (current_time - em.timestamp).total_seconds() < 60]
    city_state["emergencies"] = active_emergencies

    if random.random() < 0.05:
        event = EmergencyEvent(
            event_type=random.choice(list(EventType)),
            severity=random.choice(list(EmergencySeverity)),
            nearest_response_unit=f"Response-Unit-{random.randint(1, 5)}",
            timestamp=datetime.now(),
            location_id=random.randint(1, 10)
        )
        city_state["emergencies"].append(event)
        
def get_current_state():
    return city_state
