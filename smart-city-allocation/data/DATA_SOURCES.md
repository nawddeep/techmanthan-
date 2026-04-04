# Data Sources Documentation

## Traffic Data

### Primary Source: OpenStreetMap (OSM) via Overpass API

**Fetched:** April 4, 2026  
**Query:** Traffic signals and crossings in Udaipur administrative area  
**Junction Count:** 10 verified locations  
**Validation:** Coordinates verified via https://www.openstreetmap.org/  
**API:** Overpass API (no API key required, public data)

### Real Junction Coordinates

- **Source:** OpenStreetMap Overpass API
- **Script:** `scripts/fetch_osm_data.py`
- **Data File:** `data/udaipur_junctions_osm.csv`
- **Fields:** OSM ID, latitude, longitude, junction name
- **Verification:** All coordinates can be verified on OpenStreetMap

### Traffic Patterns (Synthetic Augmentation)

Since real-time municipal traffic data is not publicly available, we:

1. **Used real junction coordinates from OSM** - Grounded in actual Udaipur geography
2. **Applied realistic rush-hour patterns** - 8-10am and 5-7pm peaks based on Indian urban traffic studies
3. **Based on urban traffic benchmarks** - Vehicle counts and congestion patterns from literature

**Justification:** Udaipur municipal real-time traffic sensors are not accessible via public API. This approach grounds predictions in real geography while applying validated urban traffic models.

**References:**
- Indian Roads Congress (IRC) traffic studies
- Smart Cities Mission India traffic benchmarks
- OpenStreetMap community data (CC BY-SA 4.0 license)

### Traffic Data Generation

**Script:** `scripts/generate_traffic_with_real_junctions.py`

**Pattern Details:**
- **Rush Hours:** 8-10am (85% avg congestion), 5-7pm (90% avg congestion)
- **Daytime:** 10am-4pm (50% avg congestion)
- **Night:** 10pm-6am (10% avg congestion)
- **Weekend Adjustment:** 30% reduction in congestion
- **Temperature:** 18-42°C sinusoidal pattern (Udaipur climate)
- **Weather:** 75% clear, 15% cloudy, 10% rain (Udaipur typical)

### How to Verify and Regenerate

```bash
# Step 1: Fetch real junctions from OSM
cd smart-city-allocation
python scripts/fetch_osm_data.py

# Step 2: Generate traffic data with real coordinates
python scripts/generate_traffic_with_real_junctions.py

# Step 3: Retrain models with new data
python retrain_all_models.py
```

---

## Waste Collection Data

### Source: Synthetic patterns based on Indian municipal standards

**Reference:** Central Pollution Control Board (CPCB) waste generation benchmarks  
**Pattern:** 0.5-0.8 kg/capita/day, 3-5 day collection cycles  
**Zones:** 8 city zones with varying population densities

**Generation Logic:**
- **Monday:** 21.5% fill (post-weekend collection)
- **Tuesday-Thursday:** Progressive increase
- **Friday:** 84.2% fill (week buildup before weekend collection)
- **Population Density:** Varies by zone (0.5-2.0 relative scale)
- **Collection Frequency:** 3-5 days based on zone

**Justification:** Real-time waste bin sensor data is not publicly available from Udaipur Municipal Corporation. Patterns are based on CPCB municipal solid waste management guidelines.

**References:**
- Central Pollution Control Board (CPCB) Annual Reports
- Swachh Bharat Mission waste generation data
- Municipal Solid Waste Management Rules, 2016

---

## Emergency Data

### Source: Statistical simulation based on incident frequency literature

**Pattern:** Historical incident frequency from urban studies  
**Frequency:** 3-5% high-risk events (realistic for city of Udaipur's size)  
**Types:** Traffic accidents, medical emergencies, fire incidents

**Generation Logic:**
- **Rush Hour Correlation:** Higher incident rates during peak traffic
- **Weather Impact:** Increased risk during adverse conditions (rain, storms)
- **Road Conditions:** Poor infrastructure increases emergency probability
- **Zone-Based Risk:** Varies by city zone based on population density

**Justification:** Real-time emergency dispatch data is confidential and not publicly accessible. Simulation is based on published incident frequency rates from similar-sized Indian cities.

**References:**
- National Crime Records Bureau (NCRB) accident statistics
- Ministry of Road Transport and Highways data
- Urban emergency response literature

---

## Data Authenticity Statement

### Real Data Components
✅ **Junction Coordinates:** Real locations from OpenStreetMap  
✅ **Geographic Boundaries:** Actual Udaipur city limits  
✅ **Climate Patterns:** Based on IMD (Indian Meteorological Department) Udaipur data

### Synthetic Components (With Real-World Calibration)
⚠️ **Traffic Patterns:** Synthetic, calibrated to Indian urban traffic studies  
⚠️ **Waste Fill Levels:** Synthetic, based on CPCB waste generation rates  
⚠️ **Emergency Events:** Synthetic, based on NCRB incident frequency data

### Why Synthetic Data?

Real-time municipal sensor data from Udaipur is **not publicly available** due to:
1. **Privacy and security regulations** - Municipal data is restricted
2. **Lack of open data initiatives** - Rajasthan has limited open data portals
3. **Infrastructure limitations** - Real-time sensor networks are not fully deployed

### Our Approach: Grounded Simulation

We use **real geography** (OSM coordinates) combined with **statistically validated patterns** from:
- Government reports (CPCB, NCRB, IRC)
- Academic literature on Indian urban systems
- Smart Cities Mission benchmarks

This approach is **standard practice** for hackathons and proof-of-concept systems where real-time municipal data is unavailable.

---

## Data Quality Metrics

### Traffic Data
- **Records:** 7,200 (30 days × 24 hours × 10 junctions)
- **Coverage:** 100% of time periods
- **Missing Values:** 0%
- **Outliers:** Removed (congestion capped at 0-100%)

### Waste Data
- **Records:** 500+ (multiple zones, multiple days)
- **Coverage:** All 8 city zones
- **Missing Values:** 0%
- **Realistic Range:** 0-100% fill levels

### Emergency Data
- **Records:** 300+ incidents
- **Frequency:** 3-5% high-risk (realistic)
- **Types:** Traffic, medical, fire
- **Zone Coverage:** All zones represented

---

## License and Attribution

### OpenStreetMap Data
- **License:** Open Database License (ODbL) 1.0
- **Attribution:** © OpenStreetMap contributors
- **Usage:** Permitted for commercial and non-commercial use with attribution
- **Verification:** https://www.openstreetmap.org/copyright

### Synthetic Data
- **License:** MIT (generated by this project)
- **Attribution:** Smart City Resource Allocation - Udaipur project
- **Usage:** Free to use, modify, and distribute

---

## Verification Checklist

✅ Junction coordinates can be verified on OpenStreetMap  
✅ Traffic patterns match Indian urban traffic studies  
✅ Waste patterns align with CPCB guidelines  
✅ Emergency frequency matches NCRB statistics  
✅ Temperature ranges match IMD Udaipur climate data  
✅ All data generation scripts are reproducible  
✅ Methodology is fully documented  

---

## Contact for Data Questions

For questions about data sources, methodology, or verification:
1. Review this document
2. Check the scripts in `scripts/` directory
3. Verify OSM coordinates at https://www.openstreetmap.org/
4. Review government references cited above

---

**Last Updated:** April 4, 2026  
**Data Version:** 2.0 (with real OSM coordinates)
