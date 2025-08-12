"""Communication endpoints: write, wall, and bulletin board."""
from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlmodel import Session, select

from database import get_session
from models import Message

router = APIRouter(prefix="/comm", tags=["communication"])


class SendMessageRequest(BaseModel):
    from_user: str = Field(..., min_length=1)
    to_user: Optional[str] = Field(None)
    room: Optional[str] = Field(None)
    content: str = Field(..., min_length=1, max_length=1000)


class MessageResponse(BaseModel):
    id: int
    from_user: str
    to_user: Optional[str]
    room: Optional[str]
    content: str


@router.post("/send", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def send_message(
    req: SendMessageRequest, session: Session = Depends(get_session)
) -> MessageResponse:
    if not req.to_user and not req.room:
        # It's a wall message (broadcast)
        pass
    msg = Message(
        from_user=req.from_user,
        to_user=req.to_user,
        room=req.room,
        content=req.content,
    )
    session.add(msg)
    session.commit()
    session.refresh(msg)
    return MessageResponse(**msg.model_dump())


@router.get("/inbox", response_model=List[MessageResponse])
async def list_inbox(
    username: str = Query(..., min_length=1),
    session: Session = Depends(get_session),
) -> List[MessageResponse]:
    q = select(Message).where((Message.to_user == username) | (Message.to_user.is_(None)))
    q = q.order_by(Message.created_at.desc()).limit(100)
    msgs = session.exec(q).all()
    return [MessageResponse(**m.model_dump()) for m in msgs]


@router.get("/room/{room}", response_model=List[MessageResponse])
async def list_room(room: str, session: Session = Depends(get_session)) -> List[MessageResponse]:
    q = select(Message).where(Message.room == room).order_by(Message.created_at.desc()).limit(100)
    msgs = session.exec(q).all()
    return [MessageResponse(**m.model_dump()) for m in msgs]
