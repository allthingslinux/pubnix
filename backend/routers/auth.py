"""Authentication API endpoints."""

from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.get("/")
async def auth_info():
    """Authentication information endpoint."""
    return {"message": "Authentication endpoints - TODO: Implement JWT auth"}


# TODO: Implement JWT authentication endpoints
# - POST /login
# - POST /logout  
# - GET /me
# - POST /refresh