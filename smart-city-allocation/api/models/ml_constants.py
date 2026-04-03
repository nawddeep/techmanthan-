"""Centralized feature column definitions to align training and inference."""

TRAFFIC_FEATURES = [
    "hour",
    "day_enc",
    "junction_enc",
    "weather_enc",
    "temperature_c",
    "vehicles",
]

WASTE_FEATURES = [
    "area",
    "day_of_week",
    "population_density",
    "last_collection_days",
    "bin_fill_pct",
]

EMERGENCY_FEATURES = [
    "zone",
    "hour",
    "day_of_week",
    "weather",
    "road_condition",
]

# Mapping from raw data column names to API-aligned names
TRAFFIC_COLUMN_MAP = {
    "junction": "junction_enc",
    "day_of_week": "day_enc",
    "weather": "weather_enc",
}
