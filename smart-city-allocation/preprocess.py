import pandas as pd
from sklearn.preprocessing import LabelEncoder
import os

def preprocess_data():
    # 1. Read files
    traffic_path = 'data/traffic_data.csv'
    waste_path = 'data/waste_data.csv'
    emergency_path = 'data/emergency_data.csv'
    
    traffic_df = pd.read_csv(traffic_path)
    waste_df = pd.read_csv(waste_path)
    emergency_df = pd.read_csv(emergency_path)
    
    # 2. Clean nulls
    traffic_df.fillna(method='ffill', inplace=True)
    waste_df.fillna(method='ffill', inplace=True)
    emergency_df.fillna(method='ffill', inplace=True)
    
    # 3. Encode labels
    le = LabelEncoder()
    
    # Traffic Data Categories: junction, weather
    for col in ['junction', 'weather']:
        if col in traffic_df.columns:
            traffic_df[col] = le.fit_transform(traffic_df[col].astype(str))
            
    # Waste Data Categories: area, population_density
    for col in ['area', 'population_density']:
        if col in waste_df.columns:
            waste_df[col] = le.fit_transform(waste_df[col].astype(str))
            
    # Emergency Data Categories: zone, weather, road_condition
    for col in ['zone', 'weather', 'road_condition']:
        if col in emergency_df.columns:
            emergency_df[col] = le.fit_transform(emergency_df[col].astype(str))
            
    # 4. Save clean versions
    traffic_df.to_csv('data/traffic_clean.csv', index=False)
    waste_df.to_csv('data/waste_clean.csv', index=False)
    emergency_df.to_csv('data/emergency_clean.csv', index=False)
    
    print('Clean versions successfully saved in data/ folder')

if __name__ == "__main__":
    if os.path.exists('data'):
        preprocess_data()
    else:
        print('Error: data/ directory not found.')
