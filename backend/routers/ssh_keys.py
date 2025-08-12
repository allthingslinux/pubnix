"""API endpoints for SSH key management."""
from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from pydantic import BaseModel, Field
from sqlmodel import Session, select

from database import get_session
from models import SshKey, User
from services.ssh_key_service import SshKeyService
from services.audit_logger import AuditLogger

router = APIRouter(prefix="/ssh-keys", tags=["ssh-keys"])


class SshKeyCreate(BaseModel):
    username: str = Field(..., description="Owner username")
    name: str = Field(..., min_length=1, max_length=100, description="Key label")
    public_key: str = Field(..., description="OpenSSH public key line")


class SshKeyResponse(BaseModel):
    id: int
    user_id: int
    name: str
    public_key: str
    fingerprint: str
    is_active: bool


@router.post("/", response_model=SshKeyResponse, status_code=status.HTTP_201_CREATED)
async def add_ssh_key(
    key_data: SshKeyCreate, session: Session = Depends(get_session)
) -> SshKeyResponse:
    auditor = AuditLogger()
    # Ensure user exists
    user = session.exec(select(User).where(User.username == key_data.username)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Validate and fingerprint key
    try:
        parsed = SshKeyService.parse_public_key(key_data.public_key)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    # Ensure fingerprint is unique for this user
    existing = session.exec(
        select(SshKey).where(
            (SshKey.user_id == user.id) & (SshKey.fingerprint == parsed.fingerprint)
        )
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Key already exists for user"
        )

    key = SshKey(
        user_id=user.id,
        name=key_data.name,
        public_key=key_data.public_key.strip(),
        fingerprint=parsed.fingerprint,
        is_active=True,
    )
    session.add(key)
    session.commit()
    session.refresh(key)

    auditor.log(
        "ssh_key_added",
        username=user.username,
        key_id=key.id,
        fingerprint=key.fingerprint,
        name=key.name,
    )

    return SshKeyResponse(**key.model_dump())


@router.get("/", response_model=List[SshKeyResponse])
async def list_ssh_keys(
    username: Optional[str] = Query(None, description="Filter by username"),
    session: Session = Depends(get_session),
) -> List[SshKeyResponse]:
    query = select(SshKey)
    if username:
        user = session.exec(select(User).where(User.username == username)).first()
        if not user:
            return []
        query = query.where(SshKey.user_id == user.id)
    keys = session.exec(query).all()
    return [SshKeyResponse(**k.model_dump()) for k in keys]


@router.post("/{key_id}/deactivate", response_model=SshKeyResponse)
async def deactivate_ssh_key(
    key_id: int, session: Session = Depends(get_session)
) -> SshKeyResponse:
    auditor = AuditLogger()
    key = session.get(SshKey, key_id)
    if not key:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Key not found")
    key.is_active = False
    session.add(key)
    session.commit()
    session.refresh(key)
    auditor.log("ssh_key_deactivated", key_id=key.id, fingerprint=key.fingerprint)
    return SshKeyResponse(**key.model_dump())


@router.delete("/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ssh_key(
    key_id: int, session: Session = Depends(get_session)
) -> Response:
    auditor = AuditLogger()
    key = session.get(SshKey, key_id)
    if not key:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Key not found")
    session.delete(key)
    session.commit()
    auditor.log("ssh_key_deleted", key_id=key_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
