"""Application submission and management API endpoints."""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlmodel import Session, select

from database import get_session
from models import Application, ApplicationStatus, User, UserStatus, ResourceLimits
from services.email_service import EmailService
from services.validation_service import ValidationService

router = APIRouter(prefix="/applications", tags=["applications"])


def get_current_admin_username() -> str:
    """Temporary admin identity dependency placeholder.

    TODO: Replace with real JWT-based admin auth when auth is implemented.
    """
    return "admin"


class ApplicationCreate(BaseModel):
    """Application creation request model."""
    
    email: EmailStr = Field(..., description="Applicant email address")
    username_requested: str = Field(
        ...,
        min_length=3,
        max_length=32,
        pattern=r"^[a-zA-Z0-9_]+$",
        description="Requested username (3-32 chars, alphanumeric + underscore)",
    )
    full_name: str = Field(..., min_length=1, max_length=100, description="Full name")
    motivation: Optional[str] = Field(
        None, max_length=1000, description="Why you want an account"
    )
    community_guidelines_accepted: bool = Field(
        ..., description="Must accept community guidelines"
    )


class ApplicationResponse(BaseModel):
    """Application response model."""
    
    id: int
    email: str
    username_requested: str
    full_name: str
    motivation: Optional[str]
    community_guidelines_accepted: bool
    application_date: datetime
    status: ApplicationStatus
    reviewed_by: Optional[str]
    review_date: Optional[datetime]
    review_notes: Optional[str]


class ApplicationReview(BaseModel):
    """Application review request model."""
    
    status: ApplicationStatus = Field(..., description="Review decision")
    review_notes: Optional[str] = Field(
        None, max_length=500, description="Admin review notes"
    )


@router.post("/", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
async def submit_application(
    application_data: ApplicationCreate,
    session: Session = Depends(get_session),
) -> ApplicationResponse:
    """Submit a new application for account approval."""
    
    # Validate community guidelines acceptance
    if not application_data.community_guidelines_accepted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Community guidelines must be accepted",
        )
    
    # Check if email already has an application
    existing_app = session.exec(
        select(Application).where(Application.email == application_data.email)
    ).first()
    
    if existing_app:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An application already exists for this email address",
        )
    
    # Check if username is already taken or requested
    username_taken = session.exec(
        select(User).where(User.username == application_data.username_requested)
    ).first()
    
    if username_taken:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username is already taken",
        )
    
    username_requested = session.exec(
        select(Application).where(
            Application.username_requested == application_data.username_requested
        )
    ).first()
    
    if username_requested:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username is already requested by another application",
        )
    
    # Validate application fields
    validation_service = ValidationService()
    if not validation_service.validate_username(application_data.username_requested):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username format",
        )
    if not validation_service.validate_email(application_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format",
        )
    if not validation_service.validate_full_name(application_data.full_name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid full name",
        )
    
    # Create new application
    application = Application(
        email=application_data.email,
        username_requested=application_data.username_requested,
        full_name=application_data.full_name,
        motivation=application_data.motivation,
        community_guidelines_accepted=application_data.community_guidelines_accepted,
    )
    
    session.add(application)
    session.commit()
    session.refresh(application)
    
    # Send confirmation email
    email_service = EmailService()
    await email_service.send_application_confirmation(application)
    
    return ApplicationResponse.model_validate(application, from_attributes=True)


@router.get("/", response_model=List[ApplicationResponse])
async def list_applications(
    status_filter: Optional[ApplicationStatus] = None,
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
) -> List[ApplicationResponse]:
    """List applications with optional status filtering."""
    
    query = select(Application)
    
    if status_filter:
        query = query.where(Application.status == status_filter)
    
    query = query.offset(skip).limit(limit).order_by(Application.application_date.desc())
    
    applications = session.exec(query).all()
    
    return [
        ApplicationResponse.model_validate(app, from_attributes=True)
        for app in applications
    ]


@router.get("/{application_id}", response_model=ApplicationResponse)
async def get_application(
    application_id: int,
    session: Session = Depends(get_session),
) -> ApplicationResponse:
    """Get a specific application by ID."""
    
    application = session.get(Application, application_id)
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )
    
    return ApplicationResponse.model_validate(application, from_attributes=True)


@router.patch("/{application_id}/review", response_model=ApplicationResponse)
async def review_application(
    application_id: int,
    review_data: ApplicationReview,
    session: Session = Depends(get_session),
    admin_username: str = Depends(get_current_admin_username),
) -> ApplicationResponse:
    """Review an application (admin only)."""
    
    application = session.get(Application, application_id)
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )
    
    if application.status != ApplicationStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Application has already been reviewed",
        )
    
    # Update application status
    application.status = review_data.status
    application.review_notes = review_data.review_notes
    application.review_date = datetime.utcnow()
    application.reviewed_by = admin_username
    application.updated_at = datetime.utcnow()
    
    session.add(application)
    session.commit()
    session.refresh(application)
    
    # Send notification email
    email_service = EmailService()
    await email_service.send_application_status_update(application)
    
    # If approved, create user account
    if review_data.status == ApplicationStatus.APPROVED:
        # Check if user already exists (idempotency)
        existing_user = session.exec(
            select(User).where(User.username == application.username_requested)
        ).first()

        if existing_user is None:
            user = User(
                username=application.username_requested,
                email=application.email,
                full_name=application.full_name,
                status=UserStatus.APPROVED,
                approval_date=application.review_date,
                created_by=admin_username,
            )
            session.add(user)
            session.commit()
            session.refresh(user)

            # Create default resource limits for the user
            limits = ResourceLimits(user_id=user.id)
            session.add(limits)
            session.commit()
    
    return ApplicationResponse.model_validate(application, from_attributes=True)