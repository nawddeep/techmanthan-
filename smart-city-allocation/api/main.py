import asyncio
import logging
import os
import time
from contextlib import asynccontextmanager
from datetime import datetime

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from starlette.middleware.base import BaseHTTPMiddleware

load_dotenv()

from api.db.database import init_db
from api.db import persistence
from api.routes import (
    alerts,
    auth,
    emergency,
    explain,
    history,
    map_data,
    models_route,
    system,
    traffic,
    waste,
    ws,
)
from api.services.emergency_ml_service import load_emergency_model
from api.services.ml_service import load_models
from api.services.simulation_service import run_simulation

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("smartcity")

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        dur = (time.time() - start) * 1000
        logger.info(
            "%s %s -> %s %.1fms",
            request.method,
            request.url.path,
            response.status_code,
            dur,
        )
        return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing database...")
    os.makedirs(os.path.join(os.path.dirname(__file__), "..", "data"), exist_ok=True)
    init_db()
    persistence.mark_ready()
    load_models()
    load_emergency_model()
    asyncio.create_task(run_simulation())
    yield


app = FastAPI(
    title="Smart City Command Center API",
    description="AI-driven resource allocation for Udaipur: traffic, waste, emergency risk, "
    "with JWT auth, SQLite history, WebSocket city updates, and SHAP explainability.",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in ALLOWED_ORIGINS if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestLoggingMiddleware)

startup_time = datetime.now()


@app.get("/health", tags=["Health"])
def health_check():
    from api.services import emergency_ml_service as ems
    from api.services.ml_service import _traffic_model, _waste_model

    uptime_seconds = (datetime.now() - startup_time).total_seconds()
    db_ok = persistence.ping_db()

    return {
        "status": "healthy" if db_ok else "degraded",
        "timestamp": datetime.now().isoformat(),
        "uptime_minutes": round(uptime_seconds / 60, 1),
        "database": db_ok,
        "models_loaded": {
            "traffic": _traffic_model is not None,
            "waste": _waste_model is not None,
            "emergency": ems._emergency_model is not None,
        },
        "simulation_running": True,
        "api_version": "2.0.0",
    }


@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Smart City Command Center API", "docs": "/api/docs"}


@app.get("/api/data-sources", tags=["Metadata"])
def get_data_sources():
    return {
        "training_data": "data/*_clean.csv",
        "simulation": "RealDataSimulator with CSV sampling",
        "auth": "JWT bearer + refresh",
    }


app.include_router(auth.router)
app.include_router(traffic.router)
app.include_router(waste.router)
app.include_router(emergency.router)
app.include_router(alerts.router)
app.include_router(map_data.router)
app.include_router(system.router)
app.include_router(history.router)
app.include_router(explain.router)
app.include_router(models_route.router)
app.include_router(ws.router)
