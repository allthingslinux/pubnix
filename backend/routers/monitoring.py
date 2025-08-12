"""Monitoring endpoints: Prometheus metrics and simple alerts stub."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Response
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
    Gauge,
    generate_latest,
)

router = APIRouter(prefix="/monitoring", tags=["monitoring"])


@router.get("/metrics")
async def prometheus_metrics() -> Response:
    registry = CollectorRegistry()
    # Example gauges; in production, hook to real collectors
    g_users = Gauge("pubnix_total_users", "Total users", registry=registry)
    g_users.set(0)
    g_apps = Gauge(
        "pubnix_pending_applications", "Pending applications", registry=registry
    )
    g_apps.set(0)
    output = generate_latest(registry)
    return Response(content=output, media_type=CONTENT_TYPE_LATEST)


@router.get("/alerts/health")
async def simple_health_alert() -> dict[str, Any]:
    # Stub: would evaluate recent metrics and raise alerts
    return {"status": "ok"}
