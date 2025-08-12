"""Administrative endpoints for ATL Pubnix."""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlmodel import Session, col, select

from database import get_session
from models import (
    Application,
    ApplicationStatus,
    ResourceLimits,
    SshKey,
    SystemMetrics,
    User,
    UserStatus,
)
from services.metrics_collector import MetricsCollector

router = APIRouter(prefix="/admin", tags=["admin"])


def get_current_admin_username() -> str:
    # TODO: integrate JWT admin auth
    return "admin"


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    status: UserStatus
    approval_date: Optional[datetime]


@router.get("/users", response_model=List[UserResponse])
async def list_users(
    status_filter: Optional[UserStatus] = Query(None),
    q: Optional[str] = Query(None, description="Search by username/email"),
    limit: int = Query(100, ge=1, le=500),
    session: Session = Depends(get_session),
    admin: str = Depends(get_current_admin_username),
) -> List[UserResponse]:
    query = select(User)
    if status_filter is not None:
        query = query.where(User.status == status_filter)
    if q:
        like = f"%{q}%"
        query = query.where((col(User.username).like(like)) | (col(User.email).like(like)))
    query = query.order_by(User.created_at.desc()).limit(limit)
    users = session.exec(query).all()
    return [UserResponse(**u.model_dump()) for u in users]


class SuspendRequest(BaseModel):
    reason: Optional[str] = Field(None, max_length=200)


@router.post("/users/{user_id}/suspend", response_model=UserResponse)
async def suspend_user(
    user_id: int,
    req: SuspendRequest,
    session: Session = Depends(get_session),
    admin: str = Depends(get_current_admin_username),
) -> UserResponse:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.status = UserStatus.SUSPENDED
    user.updated_at = datetime.utcnow()
    session.add(user)
    session.commit()
    session.refresh(user)
    return UserResponse(**user.model_dump())


@router.post("/users/{user_id}/unsuspend", response_model=UserResponse)
async def unsuspend_user(
    user_id: int,
    session: Session = Depends(get_session),
    admin: str = Depends(get_current_admin_username),
) -> UserResponse:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.status != UserStatus.SUSPENDED:
        raise HTTPException(status_code=400, detail="User is not suspended")
    user.status = UserStatus.APPROVED
    user.updated_at = datetime.utcnow()
    session.add(user)
    session.commit()
    session.refresh(user)
    return UserResponse(**user.model_dump())


class LimitsPatch(BaseModel):
    disk_quota_mb: Optional[int] = Field(None, ge=100)
    max_processes: Optional[int] = Field(None, ge=1)
    cpu_limit_percent: Optional[int] = Field(None, ge=1, le=100)
    memory_limit_mb: Optional[int] = Field(None, ge=64)
    max_login_sessions: Optional[int] = Field(None, ge=1)


@router.patch("/users/{user_id}/limits", response_model=Dict[str, Any])
async def update_user_limits(
    user_id: int,
    patch: LimitsPatch,
    session: Session = Depends(get_session),
    admin: str = Depends(get_current_admin_username),
) -> Dict[str, Any]:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    limits = session.exec(select(ResourceLimits).where(ResourceLimits.user_id == user_id)).first()
    if limits is None:
        limits = ResourceLimits(user_id=user_id)

    for field, value in patch.model_dump(exclude_none=True).items():
        setattr(limits, field, value)
    limits.updated_at = datetime.utcnow()

    session.add(limits)
    session.commit()
    session.refresh(limits)

    return {"user_id": user_id, "limits": limits.model_dump()}


class HealthResponse(BaseModel):
    system: Dict[str, Any]
    summary: Dict[str, int]


@router.get("/health", response_model=HealthResponse)
async def system_health(
    session: Session = Depends(get_session),
    admin: str = Depends(get_current_admin_username),
) -> HealthResponse:
    # Summary counts
    total_users = session.exec(select(User)).all()
    total_users_count = len(total_users)
    approved_count = sum(1 for u in total_users if u.status == UserStatus.APPROVED)
    pending_apps = session.exec(
        select(Application).where(Application.status == ApplicationStatus.PENDING)
    ).all()
    total_ssh_keys = len(session.exec(select(SshKey)).all())

    # System metrics snapshot
    collector = MetricsCollector()
    sys = collector.collect_system_metrics().model_dump()

    return HealthResponse(
        system=sys,
        summary={
            "total_users": total_users_count,
            "approved_users": approved_count,
            "pending_applications": len(pending_apps),
            "ssh_keys": total_ssh_keys,
        },
    )
