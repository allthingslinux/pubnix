from services.resource_enforcer import ResourceEnforcer, Violation
from models import ResourceLimits, UserMetrics


def test_detects_violations():
    limits = ResourceLimits(
        user_id=1,
        disk_quota_mb=100,
        max_processes=5,
        cpu_limit_percent=10,
        memory_limit_mb=50,
        max_login_sessions=2,
    )
    metrics = UserMetrics(
        username="alice",
        cpu_time_seconds=0,
        memory_usage_mb=200,
        disk_usage_mb=500,
        active_processes=10,
        login_sessions=4,
    )
    enforcer = ResourceEnforcer()
    violations = enforcer.check_user_violations(metrics, limits)
    kinds = sorted(v.kind for v in violations)
    assert kinds == ["disk", "memory", "processes", "sessions"]


def test_build_enforcement_commands():
    enforcer = ResourceEnforcer()
    violations = [
        Violation(kind="processes", value=10, limit=5, message=""),
        Violation(kind="memory", value=200, limit=50, message=""),
        Violation(kind="sessions", value=5, limit=2, message=""),
        Violation(kind="disk", value=1000, limit=100, message=""),
    ]
    cmds = enforcer.build_enforcement_commands("alice", violations)
    assert any("renice" in c for c in cmds)
    assert any("logger" in c for c in cmds)
