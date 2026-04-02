# Smart City Resource Allocation — Udaipur

AI-assisted command center for traffic congestion, waste overflow, and emergency risk, built for hackathon demos with a **FastAPI** backend, **Next.js** dashboard, **SQLite** history, **JWT** auth, and **scikit-learn / XGBoost** models with **SHAP** explanations.

## Architecture (ASCII)

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────────────────┐
│  Next.js    │────▶│ Next Route Handlers │───▶│ FastAPI (JWT, rate limit)  │
│  Dashboard  │     │ /api/bff/* + login  │    │ /predict /explain /system  │
└──────┬──────┘     └──────────────────┘     └──────────────┬──────────────┘
       │ httpOnly cookie                                      │
       │                                                     ▼
       │ WebSocket (optional)                         ┌──────────────┐
       └──────────────────────────────────────────────│ SQLite DB    │
                                                      │ city_metrics │
                                                      │ decisions    │
                                                      └──────────────┘
                               ┌──────────────────────────────┐
                               │ CSV-backed RealDataSimulator │
                               │ traffic / waste / emergency  │
                               └──────────────────────────────┘
```

## Setup

### 1. Backend

```bash
cd smart-city-allocation
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
cp .env.example .env        # set SECRET_KEY to a long random string
pip install -r requirements.txt
# Train models (optional if pkl already present)
jupyter execute notebooks/train_models.ipynb   # or run cells in Jupyter
alembic upgrade head                         # optional; init_db() also creates tables
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

Open API docs: `http://127.0.0.1:8000/api/docs`

### 2. Frontend

```bash
cd frontend
cp .env.local.example .env.local
npm install
npm run dev
```

Visit `http://localhost:3000/login` — demo users: **admin / admin123** (full POST to predict/explain), **viewer / viewer123** (GET only).

### 3. Demo script

```bash
export API_URL=http://127.0.0.1:8000
python demo/demo_script.py
```

## ML pipeline

1. Clean CSVs: `data/traffic_clean.csv`, `waste_clean.csv`, `emergency_clean.csv`.
2. Notebook `notebooks/train_models.ipynb` runs EDA, stratified splits, RF / GB / XGB benchmarks, saves `traffic_model.pkl`, `waste_model.pkl`, `emergency_model.pkl` and plots under `notebooks/plots/`.
3. Inference uses **sklearn Pipelines** (`StandardScaler` + tree model) so preprocessing matches training.
4. **SHAP** (`explainability_service.py`) uses the tree sub-estimator on transformed features.

## Retraining

Run the notebook end-to-end, then restart the API so `joblib` reloads pickles.

## API reference (selected)

| Method | Path | Auth |
|--------|------|------|
| POST | `/auth/token` | Public (OAuth2 form) |
| POST | `/auth/refresh` | Refresh body |
| GET | `/auth/me` | Bearer |
| GET | `/health` | Public |
| GET | `/system/decision` | Bearer |
| POST | `/predict/traffic`, `/predict/waste` | Admin |
| POST | `/explain/traffic`, `/explain/waste` | Admin |
| GET | `/map-data`, `/history/trends`, `/history/full`, `/models/stats` | Bearer |
| WS | `/ws/city-updates` | Public (demo) |

## Screenshots

_Add dashboard, model stats, and map screenshots here for your submission._

## Team

_Add your hackathon team names and roles._

## Docker

```bash
docker compose up --build
```

Ensure model `.pkl` files are present or mount them as in `docker-compose.yml`.
