"""Main FastAPI application for ATL Pubnix backend services."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import create_db_and_tables
from routers import applications, auth
from routers import web as web_routes
from routers import ssh_keys
from routers import comm as comm_routes
from routers import admin as admin_routes


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager."""
    # Startup
    create_db_and_tables()
    yield
    # Shutdown
    pass


# Create FastAPI application
app = FastAPI(
    title="ATL Pubnix API",
    description="Backend API for ATL Pubnix public access Unix system",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(applications.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(web_routes.router)
app.include_router(ssh_keys.router, prefix="/api/v1")
app.include_router(comm_routes.router, prefix="/api/v1")
app.include_router(admin_routes.router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "ATL Pubnix API", "version": "0.1.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )