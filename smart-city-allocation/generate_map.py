import pandas as pd
import folium
from folium.plugins import HeatMap

def main():
    # Load data
    traffic = pd.read_csv('data/traffic_data.csv')
    waste = pd.read_csv('data/waste_data.csv')
    emergency = pd.read_csv('data/emergency_data.csv')
    
    # Udaipur Coordinates from PRD
    junction_coords = {
        'Delhi Gate': [24.5772, 73.7156],
        'Surajpol': [24.5852, 73.7219],
        'Hiran Magri': [24.6108, 73.6891],
        'Sector 11 Chauraha': [24.6032, 73.6978],
        'Madhuban': [24.5924, 73.7089],
        'Bhupalpura': [24.5712, 73.7301],
        'Pratap Nagar': [24.5631, 73.7198],
        'Bedla Road': [24.6201, 73.6845]
    }
    
    area_coords = {
        'Hiran Magri': [24.6108, 73.6891],
        'Sector 4': [24.6071, 73.6923],
        'Sector 11': [24.6032, 73.6978],
        'Bhupalpura': [24.5712, 73.7301],
        'Madhuban': [24.5924, 73.7089],
        'Pratap Nagar': [24.5631, 73.7198],
        'Shastri Circle': [24.5891, 73.7134],
        'Chetak Circle': [24.5841, 73.7112]
    }
    
    zone_coords = {
        'Delhi Gate Zone': [24.5772, 73.7156],
        'Hiran Magri Zone': [24.6108, 73.6891],
        'City Station Zone': [24.5901, 73.7198],
        'Bhupalpura Zone': [24.5712, 73.7301],
        'Sukhadia Circle Zone': [24.6021, 73.7045],
        'Airport Zone': [24.6177, 73.7231]
    }
    
    # Map Center: Udaipur [24.5854, 73.7125] zoom 13
    m = folium.Map(location=[24.5854, 73.7125], zoom_start=13)
    
    # Layer 1: Red HeatMap using congestion_score
    heat_data = [[junction_coords[row['junction']][0], junction_coords[row['junction']][1], row['congestion_score']] 
                 for _, row in traffic.iterrows() if row['junction'] in junction_coords]
    
    # Added simple gradient parameter to emphasize Red HeatMap as requested
    HeatMap(heat_data, name='Traffic Congestion (HeatMap)', min_opacity=0.3, radius=15, 
            gradient={0.4: 'orange', 0.65: 'red', 1: 'darkred'}).add_to(m)

    # Layer 2: Orange CircleMarker for overflow_risk == 1
    waste_risk = waste[waste['overflow_risk'] == 1]
    waste_grouped = waste_risk.groupby('area').size().reset_index()
    
    fg_waste = folium.FeatureGroup(name="Waste Overflow Risk")
    for _, row in waste_grouped.iterrows():
        if row['area'] in area_coords:
            folium.CircleMarker(
                location=area_coords[row['area']],
                radius=8,
                color='orange',
                fill=True,
                fill_color='orange',
                fill_opacity=0.7,
                tooltip=f"Waste Overflow Risk: {row['area']}"
            ).add_to(fg_waste)
    fg_waste.add_to(m)

    # Layer 3: Blue plus Marker for high_risk == 1
    emergency_risk = emergency[emergency['high_risk'] == 1]
    emergency_grouped = emergency_risk.groupby('zone').size().reset_index()
    
    fg_emergency = folium.FeatureGroup(name="Emergency High Risk")
    for _, row in emergency_grouped.iterrows():
        if row['zone'] in zone_coords:
            folium.Marker(
                location=zone_coords[row['zone']],
                icon=folium.Icon(color='blue', icon='plus', prefix='fa'),
                tooltip=f"Emergency High Risk: {row['zone']}"
            ).add_to(fg_emergency)
    fg_emergency.add_to(m)

    # Add legend bottom left corner
    legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 220px; height: 130px; 
     background-color: white; z-index:9999; font-size:14px;
     border:2px solid grey; padding: 10px;">
     <b>Udaipur Map Legend</b><br>
     <i class="fa fa-circle" style="color:orange"></i> Waste Overflow Risk<br>
     <i class="fa fa-plus" style="color:blue"></i> Emergency High Risk<br>
     <i style="background:red; width: 10px; height: 10px; display: inline-block;"></i> Traffic Heatmap (Red)
     </div>
     '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # Add layer control to toggle feature groups
    folium.LayerControl().add_to(m)

    # Save to file
    m.save('map.html')
    print("Map successfully generated and saved as map.html")

if __name__ == "__main__":
    main()
