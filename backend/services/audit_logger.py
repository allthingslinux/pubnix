"""Structured audit logging for security events."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import structlog


class AuditLogger:
    def __init__(self) -> None:
        self.logger = structlog.get_logger("audit")

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def log(self, event_name: str, **kwargs: Any) -> None:
        payload: dict[str, Any] = {"ts": self._now(), "evt": event_name}
        payload.update(kwargs)
        # Emit structured line; in production, route to file/syslog
        self.logger.info("audit", **payload)
