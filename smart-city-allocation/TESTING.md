# Testing Guide

## Quick Start

### Run All Tests:
```bash
cd smart-city-allocation
source .venv/bin/activate
python -m pytest tests/ -v
```

### Expected Output:
```
====================================================== 22 passed in 1.93s ======================================================
```

---

## Test Files

### 1. test_ml_pipeline.py (8 tests)
Tests ML models, predictions, and feature alignment.

```bash
python -m pytest tests/test_ml_pipeline.py -v
```

**Tests:**
- Model loading
- Prediction probability ranges (0-1)
- Feature list consistency
- Edge case handling

### 2. test_api_routes.py (6 tests)
Tests API endpoints return 200 and valid responses.

```bash
python -m pytest tests/test_api_routes.py -v
```

**Tests:**
- /health endpoint
- /system/decision endpoint
- /map-data endpoint
- Response structure validation

### 3. test_decision_engine.py (8 tests)
Tests health score formula and decision logic.

```bash
python -m pytest tests/test_decision_engine.py -v
```

**Tests:**
- Clean city = 100 score
- High traffic/waste lowers score
- Score never negative
- Emergencies and alerts deduct points

---

## Test Coverage

### Total: 22 tests
- ✅ ML Pipeline: 8 tests
- ✅ API Routes: 6 tests
- ✅ Decision Engine: 8 tests

### Pass Rate: 100%
All tests passing, no failures.

---

## Requirements

```bash
pip install pytest requests
```

---

## CI/CD Integration

Add to your CI pipeline:
```yaml
- name: Run tests
  run: |
    source .venv/bin/activate
    python -m pytest tests/ -v --tb=short
```

---

## Troubleshooting

### Server Not Running
If API tests fail, ensure server is running:
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

### Import Errors
Ensure you're in the correct directory:
```bash
cd smart-city-allocation
source .venv/bin/activate
```

### Model Not Found
Ensure models are trained:
```bash
python retrain_all_models.py
```

---

## Test Details

See `PHASE4_TESTS_COMPLETE.md` for comprehensive documentation.
