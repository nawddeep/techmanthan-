# 🟡 PHASE B: POLISH & CREDIBILITY

**Time Required:** 20 minutes  
**Priority:** HIGH  
**Impact:** Makes system look production-ready

---

## B1. Add Backend .env File

### Why:
Shows environment variable best practices

### What to Create:

**File:** `smart-city-allocation/.env`

```env
# Smart City Command Center - Environment Configuration
# Production deployment would use secure secret management

SECRET_KEY=smartcity_udaipur_secure_key_2024
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

API_HOST=0.0.0.0
API_PORT=8000

# External API Configuration
WEATHER_API_URL=https://api.open-meteo.com/v1/forecast
CACHE_TTL_SECONDS=300

# City Configuration
CITY_LAT=24.5854
CITY_LON=73.7125
CITY_NAME=Udaipur

# Simulation Settings
SIMULATION_TICK_INTERVAL=5
HISTORY_MAX_POINTS=50
```

### Update auth.py to use .env:

**File:** `smart-city-allocation/api/utils/auth.py`

**Add at top:**
```python
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "smartcity_udaipur_secure_key_2024")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
```

**Add to requirements.txt:**
```
python-dotenv==1.0.0
```

---

## B2. Enhance Health Check Endpoint

### Current State:
Basic health check exists but could be better

### What to Improve:

**File:** `smart-city-allocation/api/main.py`

**Replace the /health endpoint (lines 38-46) with:**

```python
from datetime import datetime

# Add at top level (after app creation)
startup_time = datetime.now()

@app.get("/health")
def health_check():
    from api.services.ml_service import _traffic_model, _waste_model
    
    uptime_seconds = (datetime.now() - startup_time).total_seconds()
    uptime_minutes = round(uptime_seconds / 60, 1)
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime_minutes": uptime_minutes,
        "models_loaded": {
            "traffic": _traffic_model is not None,
            "waste": _waste_model is not None
        },
        "simulation_running": True,
        "api_version": "1.0.0"
    }
```

---

## B3. Improve Frontend Metadata

### Why:
Professional page title and SEO

### What to Change:

**File:** `smart-city-allocation/frontend/src/app/layout.tsx`

**Update metadata:**

```tsx
export const metadata: Metadata = {
  title: "Smart City Command Center | Udaipur",
  description: "AI-powered real-time city resource allocation system for traffic management, waste collection, and emergency response optimization.",
  keywords: "smart city, AI, resource allocation, traffic management, waste management, emergency response, Udaipur",
};
```

**Add favicon (if not exists):**

In the `<head>` section of layout.tsx, add:

```tsx
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🏙️</text></svg>" />
```

---

## B4. Add robots.txt

### What to Create:

**File:** `smart-city-allocation/frontend/public/robots.txt`

```txt
User-agent: *
Allow: /

Sitemap: /sitemap.xml
```

---

## B5. Add API Documentation Link

### What to Add:

**File:** `smart-city-allocation/api/main.py`

**Update FastAPI app initialization (lines 9-13):**

```python
app = FastAPI(
    title="Smart City Command Center API",
    description="Backend AI and Data simulation engine for Smart City operations. Provides real-time decision support for traffic management, waste collection, and emergency response.",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)
```

---

## ✅ PHASE B COMPLETION CHECKLIST

After making these changes:

- [ ] .env file created with proper structure
- [ ] python-dotenv added to requirements.txt
- [ ] Health check endpoint enhanced with uptime
- [ ] Frontend metadata improved
- [ ] Favicon added
- [ ] robots.txt created
- [ ] API docs URLs configured
- [ ] All files saved

**Time Taken:** ~20 minutes  
**Next Phase:** Phase C - Demo Preparation
