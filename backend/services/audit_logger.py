"""Structured audit logging for security events."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Dict

import structlog


class AuditLogger:
    def __init__(self) -> None:
        self.logger = structlog.get_logger("audit")

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def log(self, event_name: str, **kwargs: Any) -> None:
        payload: Dict[str, Any] = {"ts": self._now(), "evt": event_name}
        payload.update(kwargs)
        # Emit structured line; in production, route to file/syslog
        self.logger.info("audit", **payload)
