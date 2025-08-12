"""Resource limit enforcement for ATL Pubnix users."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from models import ResourceLimits, UserMetrics


@dataclass
class Violation:
    kind: str
    value: int | float
    limit: int | float
    message: str


class ResourceEnforcer:
    """Checks user metrics against limits and proposes enforcement actions."""

    def check_user_violations(
        self, metrics: UserMetrics, limits: ResourceLimits
    ) -> List[Violation]:
        violations: List[Violation] = []

        if metrics.active_processes > limits.max_processes:
            violations.append(
                Violation(
                    kind="processes",
                    value=metrics.active_processes,
                    limit=limits.max_processes,
                    message="Too many active processes",
                )
            )

        if metrics.memory_usage_mb > limits.memory_limit_mb:
            violations.append(
                Violation(
                    kind="memory",
                    value=metrics.memory_usage_mb,
                    limit=limits.memory_limit_mb,
                    message="Memory usage exceeds limit",
                )
            )

        if metrics.login_sessions > limits.max_login_sessions:
            violations.append(
                Violation(
                    kind="sessions",
                    value=metrics.login_sessions,
                    limit=limits.max_login_sessions,
                    message="Too many concurrent sessions",
                )
            )

        if metrics.disk_usage_mb > limits.disk_quota_mb:
            violations.append(
                Violation(
                    kind="disk",
                    value=metrics.disk_usage_mb,
                    limit=limits.disk_quota_mb,
                    message="Disk usage exceeds quota",
                )
            )

        return violations

    def build_enforcement_commands(self, username: str, violations: List[Violation]) -> List[str]:
        """Return shell commands that would mitigate the violations.

        These are conservative defaults; production may replace with more nuanced actions.
        """
        cmds: List[str] = []
        kinds = {v.kind for v in violations}
        if "processes" in kinds or "memory" in kinds:
            # Reduce process impact; as a safe default, lower priority for all user procs
            cmds.append(f"renice +10 -u {username}")
        if "sessions" in kinds:
            # As a placeholder, log a warning (real system would kick excess sessions via PAM)
            cmds.append(f"logger 'Excess sessions for {username}'")
        if "disk" in kinds:
            # Suggest applying soft quota; real management would use setquota
            cmds.append(f"# setquota -u {username} <soft> <hard> 0 0 /home")
        return cmds
