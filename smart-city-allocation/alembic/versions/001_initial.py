"""initial schema

Revision ID: 001
Revises:
Create Date: 2026-04-03

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "city_metrics",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
        sa.Column("location_id", sa.Integer(), nullable=True),
        sa.Column("traffic_level", sa.Float(), nullable=True),
        sa.Column("waste_level", sa.Float(), nullable=True),
        sa.Column("data_source", sa.String(length=32), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_city_metrics_timestamp", "city_metrics", ["timestamp"], unique=False)
    op.create_index("ix_city_metrics_location_id", "city_metrics", ["location_id"], unique=False)

    op.create_table(
        "emergency_events",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
        sa.Column("zone", sa.Integer(), nullable=True),
        sa.Column("risk_score", sa.Float(), nullable=True),
        sa.Column("high_risk", sa.Boolean(), nullable=True),
        sa.Column("event_type", sa.String(length=64), nullable=True),
        sa.Column("severity", sa.String(length=32), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_emergency_events_timestamp", "emergency_events", ["timestamp"], unique=False)
    op.create_index("ix_emergency_events_zone", "emergency_events", ["zone"], unique=False)

    op.create_table(
        "system_decisions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
        sa.Column("city_health_score", sa.Float(), nullable=True),
        sa.Column("max_traffic", sa.Float(), nullable=True),
        sa.Column("max_waste", sa.Float(), nullable=True),
        sa.Column("actions_json", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_system_decisions_timestamp", "system_decisions", ["timestamp"], unique=False)

    op.create_table(
        "history_snapshots",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
        sa.Column("traffic", sa.Float(), nullable=True),
        sa.Column("waste", sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_history_snapshots_timestamp", "history_snapshots", ["timestamp"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_history_snapshots_timestamp", table_name="history_snapshots")
    op.drop_table("history_snapshots")
    op.drop_index("ix_system_decisions_timestamp", table_name="system_decisions")
    op.drop_table("system_decisions")
    op.drop_index("ix_emergency_events_zone", table_name="emergency_events")
    op.drop_index("ix_emergency_events_timestamp", table_name="emergency_events")
    op.drop_table("emergency_events")
    op.drop_index("ix_city_metrics_location_id", table_name="city_metrics")
    op.drop_index("ix_city_metrics_timestamp", table_name="city_metrics")
    op.drop_table("city_metrics")
