"""
API v1 Router

Combines all v1 API endpoints.
"""

from fastapi import APIRouter
from app.api.v1.endpoints import database, auth

# Create main API router
api_router = APIRouter()

# Include endpoint routers
api_router.include_router(
    database.router,
    prefix="/database",
    tags=["Database"]
)

# Future routers will be added here:
api_router.include_router(
    auth.router, 
    prefix="/auth", 
    tags=["Authentication"])
# api_router.include_router(users.router, prefix="/users", tags=["Users"])