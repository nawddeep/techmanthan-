import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import traffic, waste, emergency, alerts, map_data, auth, system, history, explain
from api.services.ml_service import load_models
from api.services.simulation_service import run_simulation

app = FastAPI(
    title="Smart City Command Center API",
    description="Backend AI and Data simulation engine for Smart City operations.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(traffic.router)
app.include_router(waste.router)
app.include_router(emergency.router)
app.include_router(alerts.router)
app.include_router(map_data.router)
app.include_router(system.router)
app.include_router(history.router)
app.include_router(explain.router)

@app.on_event("startup")
async def startup_event():
    print("Loading ML models on startup...")
    load_models()
    print("Starting background Real-Time Simulation engine...")
    asyncio.create_task(run_simulation())

@app.get("/")
def read_root():
    return {"message": "Welcome to the Smart City Command Center API"}

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "models_loaded": {
            "traffic": True,
            "waste": True
        },
        "simulation_running": True
    }
