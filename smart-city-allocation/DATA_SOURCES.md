# Data Sources & Architecture

## Overview
The Smart City Command Center uses a hybrid data architecture combining historical training data, live external APIs, and pattern-based real-time modeling.

## Data Layers

### 1. Historical Training Data
Used to train ML models for prediction and decision support.

#### Traffic Dataset
- **Records**: 2,002 entries
- **Source**: Udaipur traffic patterns
- **Features**:
  - Junction locations (Pratap Nagar, Sector 11, Hiran Magri, etc.)
  - Temporal: hour, day_of_week
  - Environmental: weather, temperature
  - Metrics: vehicles, congestion_score
- **File**: `data/traffic_data.csv`
- **Model**: Random Forest Classifier (traffic_model.pkl)

#### Waste Collection Dataset
- **Records**: 500+ entries
- **Source**: Municipal waste management records
- **Features**:
  - Area zones (Bhupalpura, Madhuban, Sector 11, etc.)
  - Temporal: day_of_week, last_collection_days
  - Metrics: population_density, bin_fill_pct, overflow_risk
- **File**: `data/waste_data.csv`
- **Model**: Random Forest Classifier (waste_model.pkl)

### 2. Live External Data
Real-time API integration with caching and fallback mechanisms.

#### Weather API (LIVE)
- **Provider**: Open-Meteo
- **Endpoint**: `https://api.open-meteo.com/v1/forecast`
- **Location**: Udaipur (24.5854°N, 73.7125°E)
- **Cache TTL**: 5 minutes
- **Status**: ✅ Active
- **Fallback**: Cached data → Simulated default

### 3. Real-Time Simulation
Pattern-based modeling using trained ML models and urban behavioral analysis.

#### Traffic Simulation
- **Method**: Time-series modeling with rush hour patterns
- **Logic**:
  - Base traffic: 50%
  - Rush hours (8-10 AM, 5-7 PM): 80%
  - Weather influence: Integrated from live API
- **Update Frequency**: Every 5 seconds
- **Blending**: 50% previous state + 50% pattern-based

#### Waste Simulation
- **Method**: Incremental fill modeling
- **Logic**:
  - Random fill rate: 0.01-0.05% per tick
  - Collection reset: 10% probability
- **Update Frequency**: Every 5 seconds

#### Emergency Events
- **Method**: Probabilistic event generation
- **Probability**: 5% per tick
- **Types**: Accident, Fire, Medical
- **Severity**: Low, Medium, High
- **Duration**: 60 seconds active window

## Production Integration Architecture

### Ready for Integration
The system is architected to seamlessly integrate with production data sources:

#### IoT Sensor Support
- **Protocols**: MQTT, REST, WebSocket
- **Integration Layer**: `external_data_service.py`
- **Features**:
  - Connection pooling
  - Automatic reconnection
  - Data validation
  - Fallback handling

#### Government API Integration
- **Target**: data.gov.in traffic and municipal APIs
- **Integration Layer**: Prepared in `external_data_service.py`
- **Function**: `fetch_government_traffic_incidents()`
- **Status**: Architecture ready, awaiting API credentials

#### Municipal Systems
- **API Gateway**: FastAPI with async support
- **Authentication**: JWT-based (expandable to OAuth2)
- **Rate Limiting**: Configurable per endpoint
- **Caching**: Redis-ready architecture

## Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     SMART CITY SYSTEM                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   LIVE API   │    │  HISTORICAL  │    │  SIMULATION  │  │
│  │   Weather    │    │  Training    │    │  Real-time   │  │
│  │   (Active)   │    │  Data (CSV)  │    │  Modeling    │  │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘  │
│         │                   │                   │            │
│         └───────────────────┼───────────────────┘            │
│                             │                                │
│                    ┌────────▼────────┐                       │
│                    │  ML MODELS      │                       │
│                    │  (Random Forest)│                       │
│                    └────────┬────────┘                       │
│                             │                                │
│                    ┌────────▼────────┐                       │
│                    │ DECISION ENGINE │                       │
│                    │ + SHAP Explain  │                       │
│                    └────────┬────────┘                       │
│                             │                                │
│                    ┌────────▼────────┐                       │
│                    │   DASHBOARD     │                       │
│                    │   (Real-time)   │                       │
│                    └─────────────────┘                       │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## Data Quality & Validation

### Training Data Quality
- ✅ Cleaned and preprocessed
- ✅ Categorical encoding applied
- ✅ Feature engineering completed
- ✅ 80-20 train-validation split
- ✅ Cross-validation performed

### Real-Time Data Quality
- ✅ Input validation on all endpoints
- ✅ Outlier detection and handling
- ✅ Missing data fallback strategies
- ✅ Data source tracking (live/cached/simulated)

## Future Enhancements

### Phase 1: IoT Integration
- Deploy traffic sensors at key junctions
- Install smart waste bins with fill sensors
- Integrate emergency response system feeds

### Phase 2: Government Data
- Connect to data.gov.in APIs
- Integrate state transport department feeds
- Municipal corporation data portals

### Phase 3: Advanced Analytics
- Predictive maintenance for infrastructure
- Anomaly detection for unusual patterns
- Long-term trend analysis and forecasting

## References

- Open-Meteo API: https://open-meteo.com/
- India Open Data: https://data.gov.in/
- Udaipur Smart City: https://udaipursmartcity.org.in/
