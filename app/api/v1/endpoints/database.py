"""
Database Test Endpoints

Endpoints to verify database connectivity and operations.
Development/testing only - remove in production.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List

from app.db.session import get_db
from app.db.models.user import User
from app.core.config import settings

router = APIRouter()


@router.get("/health")
async def database_health(db: Session = Depends(get_db)):
    """
    Check database health.
    
    Returns:
        dict: Database status and information
    """
    try:
        # Execute simple query
        result = db.execute(text("SELECT 1"))
        result.fetchone()
        
        # Get database version
        version_result = db.execute(text("SELECT version()"))
        db_version = version_result.fetchone()[0]
        
        # Count users
        user_count = db.query(User).count()
        
        return {
            "status": "healthy",
            "database": "postgresql",
            "version": db_version.split(",")[0],  # First part of version string
            "user_count": user_count,
            "pool_size": settings.DB_POOL_SIZE,
            "message": "Database is connected and operational"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed: {str(e)}"
        )


@router.get("/users/count")
async def count_users(db: Session = Depends(get_db)):
    """
    Get total user count.
    
    Returns:
        dict: Total number of users
    """
    try:
        count = db.query(User).count()
        return {
            "total_users": count,
            "message": f"Found {count} user(s) in database"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Query failed: {str(e)}"
        )


@router.get("/users/list")
async def list_users(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    List all users (paginated).
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
    
    Returns:
        dict: List of users
    """
    try:
        users = db.query(User).offset(skip).limit(limit).all()
        
        return {
            "users": [
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "is_active": user.is_active,
                    "is_superuser": user.is_superuser,
                    "created_at": user.created_at.isoformat(),
                }
                for user in users
            ],
            "total": db.query(User).count(),
            "skip": skip,
            "limit": limit
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Query failed: {str(e)}"
        )


@router.get("/tables")
async def list_tables(db: Session = Depends(get_db)):
    """
    List all database tables.
    
    Returns:
        dict: List of table names
    """
    try:
        result = db.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """))
        
        tables = [row[0] for row in result.fetchall()]
        
        return {
            "tables": tables,
            "count": len(tables),
            "schema": "public"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Query failed: {str(e)}"
        )