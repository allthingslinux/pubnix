"""Collect system and user metrics (stubbed for tests)."""

from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime, timezone
from typing import List

import psutil

from models import SystemMetrics, UserMetrics


class MetricsCollector:
    def collect_system_metrics(self) -> SystemMetrics:
        vm = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        cpu = psutil.cpu_percent(interval=None)
        net_conns = len(psutil.net_connections(kind="tcp"))
        return SystemMetrics(
            total_users=0,  # filled elsewhere
            active_users_24h=0,
            cpu_usage_percent=float(cpu),
            memory_usage_percent=float(vm.percent),
            disk_usage_percent=float(disk.percent),
            network_connections=net_conns,
            ssh_sessions=0,
            web_requests_per_hour=0,
            timestamp=datetime.now(timezone.utc),
        )

    def collect_user_metrics(self, usernames: Iterable[str]) -> List[UserMetrics]:
        now = datetime.now(timezone.utc)
        # Stub: produce zeroed metrics for each user for testing
        return [
            UserMetrics(
                username=u,
                cpu_time_seconds=0,
                memory_usage_mb=0,
                disk_usage_mb=0,
                active_processes=0,
                login_sessions=0,
                last_activity=now,
                web_requests_count=0,
                timestamp=now,
            )
            for u in usernames
        ]
