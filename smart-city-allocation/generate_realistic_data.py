#!/usr/bin/env python3
"""
Generate realistic mock data for Udaipur Smart City with proper patterns:
- Traffic: Heavy congestion 8-10am & 5-7pm, light 11pm-6am, weekday peaks at Surajpol/Delhi Gate
- Waste: Lower on Monday (post-collection), builds through Friday
- Emergency: Rare events (3-5% for high-risk, not 15%)
"""
import numpy as np
import pandas as pd
from datetime import datetime
import math

# Set seed for reproducibility
np.random.seed(42)

# Udaipur junction mapping (from map_data.py)
JUNCTIONS = {
    0: "Surajpol",          # High traffic junction
    1: "Delhi Gate",        # High traffic junction  
    2: "Pratap Nagar",
    3: "Sector 11 Chauraha",
    4: "Madhuban",
    5: "Hiran Magri",
    6: "Bedla Road",
    7: "Bhupalpura",
}

# Peak traffic junctions (Surajpol=0, Delhi Gate=1)
PEAK_JUNCTIONS = [0, 1]

def generate_traffic_data(n_samples=2000):
    """
    Generate realistic traffic data for Udaipur:
    - Heavy congestion: 8-10am and 5-7pm (rush hours)
    - Light traffic: 11pm-6am (night)
    - Weekday peaks at Surajpol and Delhi Gate
    - Temperature follows sinusoidal pattern (peaks at 2pm, range 18-42°C)
    """
    data = []
    
    for _ in range(n_samples):
        junction = np.random.choice(list(JUNCTIONS.keys()))
        hour = np.random.randint(0, 24)
        day_of_week = np.random.randint(0, 7)  # 0=Monday, 6=Sunday
        weather = np.random.choice([0, 1, 2, 3], p=[0.6, 0.25, 0.1, 0.05])  # Mostly clear
        
        # Temperature: sinusoidal pattern peaking at 14:00 (2pm)
        # Range: 18°C (night) to 42°C (afternoon) for Udaipur
        temp_base = 30.0  # Average
        temp_amplitude = 12.0  # ±12°C variation
        temp_phase = (hour - 14) / 24 * 2 * math.pi  # Peak at 14:00
        temperature_c = temp_base + temp_amplitude * math.cos(temp_phase)
        temperature_c += np.random.normal(0, 2)  # Add noise
        temperature_c = np.clip(temperature_c, 18, 42)
        
        # Base vehicle count
        vehicles = np.random.randint(50, 150)
        
        # Traffic patterns
        is_weekday = day_of_week < 5
        is_peak_junction = junction in PEAK_JUNCTIONS
        
        # Morning rush (8-10am)
        if 8 <= hour <= 10:
            vehicles += np.random.randint(200, 400)
            if is_weekday:
                vehicles += 100
            if is_peak_junction:
                vehicles += 150
        
        # Evening rush (5-7pm)
        elif 17 <= hour <= 19:
            vehicles += np.random.randint(250, 450)
            if is_weekday:
                vehicles += 120
            if is_peak_junction:
                vehicles += 180
        
        # Moderate traffic (11am-4pm, 8-10pm)
        elif (11 <= hour <= 16) or (20 <= hour <= 22):
            vehicles += np.random.randint(80, 200)
            if is_peak_junction:
                vehicles += 50
        
        # Light traffic (11pm-6am)
        elif hour >= 23 or hour <= 6:
            vehicles = np.random.randint(20, 80)
        
        # Weather impact
        if weather >= 2:  # Rain/storm
            vehicles = int(vehicles * 0.7)  # Less traffic in bad weather
        
        # Calculate congestion score (vehicles per junction capacity)
        # Capacity varies by junction
        capacity = 400 if is_peak_junction else 300
        congestion_score = (vehicles / capacity) * 10
        congestion_score += np.random.normal(0, 0.3)
        congestion_score = max(0, congestion_score)
        
        # High congestion threshold: score >= 6.0
        high_congestion = 1 if congestion_score >= 6.0 else 0
        
        data.append({
            'junction': junction,
            'hour': hour,
            'day_of_week': day_of_week,
            'weather': weather,
            'temperature_c': round(temperature_c, 1),
            'vehicles': vehicles,
            'congestion_score': round(congestion_score, 1),
            'high_congestion': high_congestion
        })
    
    df = pd.DataFrame(data)
    print(f"Traffic data generated: {len(df)} samples")
    print(f"  High congestion: {df['high_congestion'].sum()} ({df['high_congestion'].mean()*100:.1f}%)")
    print(f"  Avg vehicles: {df['vehicles'].mean():.0f}")
    print(f"  Temp range: {df['temperature_c'].min():.1f}°C - {df['temperature_c'].max():.1f}°C")
    return df


def generate_waste_data(n_samples=500):
    """
    Generate realistic waste data:
    - Lower fill on Monday (post-weekend collection)
    - Builds through the week, peaks on Friday
    - Population density affects fill rate
    """
    data = []
    
    for _ in range(n_samples):
        area = np.random.randint(0, 8)  # 8 areas
        day_of_week = np.random.randint(0, 7)
        
        # Population density: 0=low, 1=medium, 2=high
        population_density = np.random.choice([0, 1, 2], p=[0.3, 0.4, 0.3])
        
        # Days since last collection (collection happens on weekends)
        # Monday (0) = 1 day, Tuesday = 2, ..., Friday = 5, Weekend = 0-1
        if day_of_week == 0:  # Monday
            last_collection_days = np.random.choice([1, 2], p=[0.8, 0.2])
        elif day_of_week <= 4:  # Tuesday-Friday
            last_collection_days = day_of_week + np.random.randint(0, 2)
        else:  # Weekend
            last_collection_days = np.random.choice([0, 1, 6, 7], p=[0.3, 0.3, 0.2, 0.2])
        
        # Base fill percentage
        bin_fill_pct = 20 + (last_collection_days * 8)  # ~8% per day
        
        # Population density impact
        if population_density == 2:  # High density
            bin_fill_pct += 15
        elif population_density == 1:  # Medium
            bin_fill_pct += 8
        
        # Day of week pattern (builds through week)
        if day_of_week == 0:  # Monday - lower (post-collection)
            bin_fill_pct *= 0.6
        elif day_of_week == 4:  # Friday - higher
            bin_fill_pct *= 1.3
        elif day_of_week >= 5:  # Weekend
            bin_fill_pct *= 1.1
        
        # Add noise
        bin_fill_pct += np.random.normal(0, 5)
        bin_fill_pct = np.clip(bin_fill_pct, 10, 100)
        
        # Overflow risk: >= 70%
        overflow_risk = 1 if bin_fill_pct >= 70 else 0
        
        data.append({
            'area': area,
            'day_of_week': day_of_week,
            'population_density': population_density,
            'last_collection_days': last_collection_days,
            'bin_fill_pct': round(bin_fill_pct, 1),
            'overflow_risk': overflow_risk
        })
    
    df = pd.DataFrame(data)
    print(f"\nWaste data generated: {len(df)} samples")
    print(f"  Overflow risk: {df['overflow_risk'].sum()} ({df['overflow_risk'].mean()*100:.1f}%)")
    print(f"  Avg fill: {df['bin_fill_pct'].mean():.1f}%")
    print(f"  Monday avg: {df[df['day_of_week']==0]['bin_fill_pct'].mean():.1f}%")
    print(f"  Friday avg: {df[df['day_of_week']==4]['bin_fill_pct'].mean():.1f}%")
    return df


def generate_emergency_data(n_samples=300):
    """
    Generate realistic emergency data:
    - RARE events: 3-5% high-risk (not 15%!)
    - More incidents during rush hours and bad weather
    - Poor road conditions increase risk
    """
    data = []
    
    for _ in range(n_samples):
        zone = np.random.randint(0, 5)  # 5 zones
        hour = np.random.randint(0, 24)
        day_of_week = np.random.randint(0, 7)
        weather = np.random.choice([0, 1, 2, 3], p=[0.6, 0.25, 0.1, 0.05])
        road_condition = np.random.choice([0, 1, 2], p=[0.7, 0.2, 0.1])  # 0=good, 1=fair, 2=poor
        
        # Base incident count (very low but not zero)
        incident_count = 0
        
        # Rush hour increases incidents slightly
        if (8 <= hour <= 10) or (17 <= hour <= 19):
            if np.random.random() < 0.25:  # 25% chance during rush
                incident_count += np.random.randint(1, 4)
        
        # Bad weather increases incidents
        if weather >= 2:  # Rain/storm
            if np.random.random() < 0.20:  # 20% chance in bad weather
                incident_count += np.random.randint(1, 3)
        
        # Poor road conditions
        if road_condition == 2:  # Poor
            if np.random.random() < 0.18:  # 18% chance
                incident_count += np.random.randint(1, 2)
        
        # Random rare incidents
        if np.random.random() < 0.10:  # 10% baseline
            incident_count += 1
        
        # Calculate risk score
        risk_score = incident_count * 0.8
        risk_score += weather * 0.4
        risk_score += road_condition * 0.6
        risk_score += np.random.normal(0, 0.5)
        risk_score = max(0, risk_score)
        
        # High risk threshold: score >= 2.5 (target 3-5% high-risk)
        high_risk = 1 if risk_score >= 2.5 else 0
        
        data.append({
            'zone': zone,
            'hour': hour,
            'day_of_week': day_of_week,
            'weather': weather,
            'road_condition': road_condition,
            'incident_count': incident_count,
            'risk_score': round(risk_score, 1),
            'high_risk': high_risk
        })
    
    df = pd.DataFrame(data)
    
    # Ensure high_risk is truly rare (3-5%)
    high_risk_pct = df['high_risk'].mean() * 100
    if high_risk_pct > 5:
        # Adjust threshold to get closer to 3-5%
        threshold = df['risk_score'].quantile(0.96)  # Top 4%
        df['high_risk'] = (df['risk_score'] >= threshold).astype(int)
        high_risk_pct = df['high_risk'].mean() * 100
    
    print(f"\nEmergency data generated: {len(df)} samples")
    print(f"  High risk: {df['high_risk'].sum()} ({high_risk_pct:.1f}%) - RARE as required!")
    print(f"  Avg incidents: {df['incident_count'].mean():.2f}")
    print(f"  Avg risk score: {df['risk_score'].mean():.2f}")
    return df


def main():
    print("="*60)
    print("Generating Realistic Udaipur Smart City Data")
    print("="*60)
    
    # Generate data
    traffic_df = generate_traffic_data(n_samples=2000)
    waste_df = generate_waste_data(n_samples=500)
    emergency_df = generate_emergency_data(n_samples=300)
    
    # Save to CSV
    traffic_df.to_csv('data/traffic_clean.csv', index=False)
    traffic_df.to_csv('data/traffic_data.csv', index=False)  # Backup
    print(f"\n✅ Saved: data/traffic_clean.csv")
    
    waste_df.to_csv('data/waste_clean.csv', index=False)
    waste_df.to_csv('data/waste_data.csv', index=False)  # Backup
    print(f"✅ Saved: data/waste_clean.csv")
    
    emergency_df.to_csv('data/emergency_clean.csv', index=False)
    emergency_df.to_csv('data/emergency_data.csv', index=False)  # Backup
    print(f"✅ Saved: data/emergency_clean.csv")
    
    print("\n" + "="*60)
    print("Data Generation Complete!")
    print("="*60)
    print("\nKey Patterns Implemented:")
    print("✅ Traffic: Heavy 8-10am & 5-7pm, light 11pm-6am")
    print("✅ Traffic: Weekday peaks at Surajpol & Delhi Gate")
    print("✅ Traffic: Temperature peaks at 2pm (18-42°C)")
    print("✅ Waste: Lower Monday, builds through Friday")
    print("✅ Emergency: RARE high-risk events (3-5%, not 15%!)")
    print("\nNext step: Retrain models with new data")
    print("  python retrain_all_models.py")
    print("="*60)


if __name__ == "__main__":
    main()
