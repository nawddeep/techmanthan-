# Smart City Resource Allocation — Udaipur

## Project Goal
AI dashboard for Udaipur city officials to predict and manage 
traffic, waste, and emergency resources.

## Files To Build
1. create_data.py
2. preprocess.py
3. train_traffic.py
4. train_waste.py
5. generate_map.py
6. app.py

## Traffic Data — data/traffic_data.csv (2000 rows)
Columns: junction, hour, day_of_week, weather, temperature_c, 
vehicles, congestion_score, high_congestion
Junctions: Delhi Gate, Surajpol, Hiran Magri, Sector 11 Chauraha, 
Madhuban, Bhupalpura, Pratap Nagar, Bedla Road
Rules:
- Morning rush hours 8,9,10 → add 150-350 vehicles
- Evening rush hours 17,18,19,20 → add 200-400 vehicles
- Rainy weather → add 50-150 vehicles
- Weekdays Mon-Fri → add 30-100 vehicles
- congestion_score = vehicles/max_vehicles * 10 rounded to 1 decimal
- high_congestion = 1 if congestion_score > 7 else 0

## Waste Data — data/waste_data.csv (500 rows)
Columns: area, day_of_week, population_density, 
last_collection_days, bin_fill_pct, overflow_risk
Areas: Hiran Magri, Sector 4, Sector 11, Bhupalpura, 
Madhuban, Pratap Nagar, Shastri Circle, Chetak Circle
Rules:
- High density areas → add 10-30 to bin_fill_pct
- last_collection_days > 4 → add 15-35 to bin_fill_pct
- clip bin_fill_pct between 0 and 100
- overflow_risk = 1 if bin_fill_pct > 75 else 0

## Emergency Data — data/emergency_data.csv (300 rows)
Columns: zone, hour, day_of_week, weather, road_condition, 
incident_count, risk_score, high_risk
Zones: Delhi Gate Zone, Hiran Magri Zone, City Station Zone, 
Bhupalpura Zone, Sukhadia Circle Zone, Airport Zone
Rules:
- Rainy weather → add 2-6 incidents
- Poor road condition → add 1-4 incidents
- Night hours 22,23,0,1,2,3 → add 1-3 incidents
- risk_score = incident_count/max_incident_count * 10 rounded to 1 decimal
- high_risk = 1 if risk_score > 6 else 0

## Map — map.html
Center: Udaipur [24.5854, 73.7125] zoom 13
Layer 1: Red HeatMap using congestion_score
Layer 2: Orange CircleMarker for overflow_risk == 1
Layer 3: Blue plus Marker for high_risk == 1
Add legend bottom left corner.

## Udaipur Coordinates
junction_coords:
- Delhi Gate: [24.5772, 73.7156]
- Surajpol: [24.5852, 73.7219]
- Hiran Magri: [24.6108, 73.6891]
- Sector 11 Chauraha: [24.6032, 73.6978]
- Madhuban: [24.5924, 73.7089]
- Bhupalpura: [24.5712, 73.7301]
- Pratap Nagar: [24.5631, 73.7198]
- Bedla Road: [24.6201, 73.6845]

area_coords:
- Hiran Magri: [24.6108, 73.6891]
- Sector 4: [24.6071, 73.6923]
- Sector 11: [24.6032, 73.6978]
- Bhupalpura: [24.5712, 73.7301]
- Madhuban: [24.5924, 73.7089]
- Pratap Nagar: [24.5631, 73.7198]
- Shastri Circle: [24.5891, 73.7134]
- Chetak Circle: [24.5841, 73.7112]

zone_coords:
- Delhi Gate Zone: [24.5772, 73.7156]
- Hiran Magri Zone: [24.6108, 73.6891]
- City Station Zone: [24.5901, 73.7198]
- Bhupalpura Zone: [24.5712, 73.7301]
- Sukhadia Circle Zone: [24.6021, 73.7045]
- Airport Zone: [24.6177, 73.7231]

## Tech Stack
pandas, numpy, scikit-learn, joblib, folium, streamlit
numpy random seed = 42

## Success Criteria
- All 3 CSV files generated in data/ folder
- Both ML models accuracy above 80%
- Map shows all 3 layers on Udaipur
- Streamlit dashboard runs with working predictions
```

---

## Step 3 — Antigravity Chat Mein Yeh Prompt Dو

PRD.md save karne ke baad Antigravity ke **AI chat** mein yeh likho:
```
Read PRD.md and create create_data.py exactly 
according to the specifications. Save it in the 
root folder. Then run it and confirm all 3 CSV 
files are created in the data/ folder.