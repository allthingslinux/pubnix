"""System and user metrics models for ATL Pubnix."""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class SystemMetrics(SQLModel, table=True):
    """System-wide metrics and health data."""

    __tablename__ = "system_metrics"

    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)
    total_users: int = Field(description="Total number of users")
    active_users_24h: int = Field(description="Users active in last 24 hours")
    cpu_usage_percent: float = Field(description="System CPU usage percentage")
    memory_usage_percent: float = Field(description="System memory usage percentage")
    disk_usage_percent: float = Field(description="System disk usage percentage")
    network_connections: int = Field(description="Active network connections")
    ssh_sessions: int = Field(default=0, description="Active SSH sessions")
    web_requests_per_hour: int = Field(
        default=0, description="Web requests in last hour"
    )

    def __str__(self) -> str:
        return (
            f"SystemMetrics(timestamp={self.timestamp}, cpu={self.cpu_usage_percent}%)"
        )


class UserMetrics(SQLModel, table=True):
    """Per-user resource usage metrics."""

    __tablename__ = "user_metrics"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, description="Username for these metrics")
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)
    cpu_time_seconds: int = Field(
        default=0, description="Total CPU time used in seconds"
    )
    memory_usage_mb: int = Field(default=0, description="Current memory usage in MB")
    disk_usage_mb: int = Field(default=0, description="Current disk usage in MB")
    active_processes: int = Field(default=0, description="Number of active processes")
    login_sessions: int = Field(
        default=0, description="Number of active login sessions"
    )
    last_activity: Optional[datetime] = Field(
        default=None, description="Last user activity"
    )
    web_requests_count: int = Field(default=0, description="Web requests served")

    def __str__(self) -> str:
        return f"UserMetrics(username={self.username}, timestamp={self.timestamp})"
