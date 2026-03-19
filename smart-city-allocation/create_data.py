import pandas as pd
import numpy as np
import os

np.random.seed(42)

def generate_traffic_data():
    n_rows = 2000
    junctions = ['Delhi Gate', 'Surajpol', 'Hiran Magri', 'Sector 11 Chauraha', 
                 'Madhuban', 'Bhupalpura', 'Pratap Nagar', 'Bedla Road']
    # Add weather options logic
    weather_conds = ['Sunny', 'Clear', 'Cloudy', 'Rainy']
    
    data = {
        'junction': np.random.choice(junctions, n_rows),
        'hour': np.random.randint(0, 24, n_rows),
        'day_of_week': np.random.randint(0, 7, n_rows), # 0=Mon, 6=Sun
        'weather': np.random.choice(weather_conds, n_rows),
        'temperature_c': np.random.uniform(15, 45, n_rows).round(1),
        'vehicles': np.random.randint(50, 200, n_rows) # Base vehicles
    }
    df = pd.DataFrame(data)
    
    # Rules
    # Morning rush hours 8,9,10 -> add 150-350 vehicles
    mask_morning = df['hour'].isin([8, 9, 10])
    df.loc[mask_morning, 'vehicles'] += np.random.randint(150, 351, mask_morning.sum())
    
    # Evening rush hours 17,18,19,20 -> add 200-400 vehicles
    mask_evening = df['hour'].isin([17, 18, 19, 20])
    df.loc[mask_evening, 'vehicles'] += np.random.randint(200, 401, mask_evening.sum())
    
    # Rainy weather -> add 50-150 vehicles
    mask_rainy = df['weather'] == 'Rainy'
    df.loc[mask_rainy, 'vehicles'] += np.random.randint(50, 151, mask_rainy.sum())
    
    # Weekdays Mon-Fri -> add 30-100 vehicles
    mask_weekday = df['day_of_week'].isin([0, 1, 2, 3, 4])
    df.loc[mask_weekday, 'vehicles'] += np.random.randint(30, 101, mask_weekday.sum())
    
    max_vehicles = df['vehicles'].max()
    df['congestion_score'] = (df['vehicles'] / max_vehicles * 10).round(1)
    df['high_congestion'] = (df['congestion_score'] > 7).astype(int)
    
    return df

def generate_waste_data():
    n_rows = 500
    areas = ['Hiran Magri', 'Sector 4', 'Sector 11', 'Bhupalpura', 
             'Madhuban', 'Pratap Nagar', 'Shastri Circle', 'Chetak Circle']
    
    density_levels = ['High', 'Medium', 'Low']
    
    data = {
        'area': np.random.choice(areas, n_rows),
        'day_of_week': np.random.randint(0, 7, n_rows),
        'population_density': np.random.choice(density_levels, n_rows),
        'last_collection_days': np.random.randint(0, 15, n_rows),
        'bin_fill_pct': np.random.uniform(10, 60, n_rows) # Base fill percentage
    }
    df = pd.DataFrame(data)
    
    # Rules
    # High density areas -> add 10-30 to bin_fill_pct
    mask_high_density = df['population_density'] == 'High'
    df.loc[mask_high_density, 'bin_fill_pct'] += np.random.uniform(10, 30, mask_high_density.sum())
    
    # last_collection_days > 4 -> add 15-35 to bin_fill_pct
    mask_delayed = df['last_collection_days'] > 4
    df.loc[mask_delayed, 'bin_fill_pct'] += np.random.uniform(15, 35, mask_delayed.sum())
    
    # clip bin_fill_pct between 0 and 100
    df['bin_fill_pct'] = df['bin_fill_pct'].clip(0, 100).round(1)
    
    # overflow_risk = 1 if bin_fill_pct > 75 else 0
    df['overflow_risk'] = (df['bin_fill_pct'] > 75).astype(int)
    
    return df

def generate_emergency_data():
    n_rows = 300
    zones = ['Delhi Gate Zone', 'Hiran Magri Zone', 'City Station Zone', 
             'Bhupalpura Zone', 'Sukhadia Circle Zone', 'Airport Zone']
    weather_conds = ['Sunny', 'Clear', 'Cloudy', 'Rainy']
    road_conds = ['Good', 'Fair', 'Poor']
    
    data = {
        'zone': np.random.choice(zones, n_rows),
        'hour': np.random.randint(0, 24, n_rows),
        'day_of_week': np.random.randint(0, 7, n_rows),
        'weather': np.random.choice(weather_conds, n_rows),
        'road_condition': np.random.choice(road_conds, n_rows),
        'incident_count': np.random.randint(0, 5, n_rows) # Base incidents
    }
    df = pd.DataFrame(data)
    
    # Rules
    # Rainy weather -> add 2-6 incidents
    mask_rainy = df['weather'] == 'Rainy'
    df.loc[mask_rainy, 'incident_count'] += np.random.randint(2, 7, mask_rainy.sum())
    
    # Poor road condition -> add 1-4 incidents
    mask_poor_road = df['road_condition'] == 'Poor'
    df.loc[mask_poor_road, 'incident_count'] += np.random.randint(1, 5, mask_poor_road.sum())
    
    # Night hours 22,23,0,1,2,3 -> add 1-3 incidents
    mask_night = df['hour'].isin([22, 23, 0, 1, 2, 3])
    df.loc[mask_night, 'incident_count'] += np.random.randint(1, 4, mask_night.sum())
    
    # risk_score = incident_count/max_incident_count * 10 rounded to 1 decimal
    max_incidents = df['incident_count'].max()
    df['risk_score'] = (df['incident_count'] / max_incidents * 10).round(1)
    
    # high_risk = 1 if risk_score > 6 else 0
    df['high_risk'] = (df['risk_score'] > 6).astype(int)
    
    return df

if __name__ == '__main__':
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    traffic_df = generate_traffic_data()
    waste_df = generate_waste_data()
    emergency_df = generate_emergency_data()
    
    traffic_df.to_csv('data/traffic_data.csv', index=False)
    waste_df.to_csv('data/waste_data.csv', index=False)
    emergency_df.to_csv('data/emergency_data.csv', index=False)
    
    print('Generated 2000 rows for traffic_data.csv')
    print('Generated 500 rows for waste_data.csv')
    print('Generated 300 rows for emergency_data.csv')
    print('All 3 CSV files successfully created in the data/ folder.')
