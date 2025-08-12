"""External integrations API for user management/provisioning."""
from __future__ import annotations

import hmac
import os
from typing import Dict, List

from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlmodel import Session, select

from database import get_session
from models import ResourceLimits, User, UserStatus

router = APIRouter(prefix="/integrations", tags=["integrations"])


def verify_token(x_api_key: str | None = Header(default=None)) -> None:
    expected = os.getenv("INTEGRATIONS_API_KEY", "dev-key")
    if not x_api_key or not hmac.compare_digest(x_api_key, expected):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


class ExternalUser(BaseModel):
    username: str = Field(..., min_length=3, max_length=32, pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr
    full_name: str


@router.post("/users/import", dependencies=[Depends(verify_token)])
async def import_users(users: List[ExternalUser], session: Session = Depends(get_session)) -> Dict[str, int]:
    created = 0
    for u in users:
        exists = session.exec(select(User).where(User.username == u.username)).first()
        if exists:
            continue
        user = User(
            username=u.username,
            email=u.email,
            full_name=u.full_name,
            status=UserStatus.APPROVED,
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        session.add(ResourceLimits(user_id=user.id))
        session.commit()
        created += 1
    return {"created": created}


@router.get("/users/export", dependencies=[Depends(verify_token)])
async def export_users(session: Session = Depends(get_session)) -> List[ExternalUser]:
    users = session.exec(select(User)).all()
    return [ExternalUser(username=u.username, email=u.email, full_name=u.full_name) for u in users]
