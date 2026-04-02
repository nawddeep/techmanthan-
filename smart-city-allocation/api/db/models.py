from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from api.db.database import Base


class CityMetric(Base):
    __tablename__ = "city_metrics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    location_id: Mapped[int] = mapped_column(Integer, index=True)
    traffic_level: Mapped[float] = mapped_column(Float)
    waste_level: Mapped[float] = mapped_column(Float)
    data_source: Mapped[str] = mapped_column(String(32), default="unknown")


class EmergencyEventRecord(Base):
    __tablename__ = "emergency_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    zone: Mapped[int] = mapped_column(Integer, index=True)
    risk_score: Mapped[float] = mapped_column(Float)
    high_risk: Mapped[bool] = mapped_column(Boolean, default=False)
    event_type: Mapped[str] = mapped_column(String(64), default="unknown")
    severity: Mapped[str] = mapped_column(String(32), default="low")


class SystemDecisionRecord(Base):
    __tablename__ = "system_decisions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    city_health_score: Mapped[float] = mapped_column(Float)
    max_traffic: Mapped[float] = mapped_column(Float)
    max_waste: Mapped[float] = mapped_column(Float)
    actions_json: Mapped[str] = mapped_column(Text)  # JSON array as string


class HistoryAggregate(Base):
    """Optional compact table for chart trends (also derivable from city_metrics)."""

    __tablename__ = "history_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    traffic: Mapped[float] = mapped_column(Float)
    waste: Mapped[float] = mapped_column(Float)
