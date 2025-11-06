"""
FastAPI Dependencies

Reusable dependencies for authentication, authorization, and database sessions.
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models.user import User
from app.db.crud.user import get_user_by_email
from app.core.security import decode_token
from app.core.config import settings


# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_PREFIX}/auth/login"
)


async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    Get current authenticated user from JWT token.
    
    This is a FastAPI dependency that:
    1. Extracts the token from Authorization header
    2. Validates the token
    3. Fetches the user from database
    4. Returns the user object
    
    Usage:
        @app.get("/protected")
        def protected_route(current_user: User = Depends(get_current_user)):
            return {"user": current_user.email}
    
    Args:
        db: Database session
        token: JWT token from Authorization header
    
    Returns:
        User: Current authenticated user
    
    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = decode_token(token)
        if payload is None:
            raise credentials_exception
        
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    user = get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current active user.
    
    Usage:
        @app.get("/me")
        def read_users_me(user: User = Depends(get_current_active_user)):
            return user
    
    Args:
        current_user: Current user from get_current_user dependency
    
    Returns:
        User: Current active user
    
    Raises:
        HTTPException: If user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


async def get_current_superuser(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current user and verify they have superuser privileges.
    
    Usage:
        @app.delete("/users/{user_id}")
        def delete_user(
            user_id: int,
            admin: User = Depends(get_current_superuser)
        ):
            # Only superusers can access this
            return {"deleted": user_id}
    
    Args:
        current_user: Current user from get_current_user dependency
    
    Returns:
        User: Current user with superuser privileges
    
    Raises:
        HTTPException: If user is not a superuser
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges"
        )
    return current_user


def get_optional_current_user(
    db: Session = Depends(get_db),
    token: Optional[str] = Depends(oauth2_scheme)
) -> Optional[User]:
    """
    Get current user if token is provided, None otherwise.
    
    Useful for endpoints that work for both authenticated and anonymous users.
    
    Usage:
        @app.get("/posts")
        def list_posts(user: Optional[User] = Depends(get_optional_current_user)):
            if user:
                # Show personalized posts
                pass
            else:
                # Show public posts
                pass
    
    Args:
        db: Database session
        token: Optional JWT token
    
    Returns:
        User if authenticated, None otherwise
    """
    if token is None:
        return None
    
    try:
        payload = decode_token(token)
        if payload is None:
            return None
        
        email: str = payload.get("sub")
        if email is None:
            return None
        
        user = get_user_by_email(db, email=email)
        return user if user and user.is_active else None
        
    except Exception:
        return None