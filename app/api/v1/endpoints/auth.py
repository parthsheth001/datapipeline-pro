"""
Authentication Endpoints

User registration, login, token refresh, and account management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.db.session import get_db
from app.db.models.user import User
from app.db.crud import user as user_crud
from app.schemas.auth import (
    UserCreate,
    UserResponse,
    Token,
    PasswordChange,
    RefreshTokenRequest
)
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_token,
    verify_password,
    get_password_hash
)
from app.core.dependencies import get_current_user, get_current_active_user
from app.core.config import settings

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user.
    
    Args:
        user_in: User registration data
        db: Database session
    
    Returns:
        UserResponse: Created user data
    
    Raises:
        HTTPException: If email or username already exists
    """
    # Check if user with email or username already exists
    existing_user = user_crud.get_user_by_email_or_username(
        db,
        email=user_in.email,
        username=user_in.username
    )
    
    if existing_user:
        if existing_user.email == user_in.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        if existing_user.username == user_in.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
    
    # Create new user
    user = user_crud.create_user(db, user_in)
    
    return user


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login with email and password to get access token.
    
    OAuth2 compatible endpoint (username field contains email).
    
    Args:
        form_data: OAuth2 password form (username=email, password)
        db: Database session
    
    Returns:
        Token: Access and refresh tokens
    
    Raises:
        HTTPException: If credentials are invalid
    """
    # Authenticate user (form_data.username contains email)
    user = user_crud.authenticate_user(
        db,
        email=form_data.username,
        password=form_data.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create tokens
    access_token = create_access_token(subject=user.email)
    refresh_token = create_refresh_token(subject=user.email)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Get new access token using refresh token.
    
    Args:
        refresh_request: Request containing refresh token
        db: Database session
    
    Returns:
        Token: New access and refresh tokens
    
    Raises:
        HTTPException: If refresh token is invalid
    """
    # Verify refresh token
    email = verify_token(refresh_request.refresh_token, token_type="refresh")
    
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user
    user = user_crud.get_user_by_email(db, email=email)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create new tokens
    access_token = create_access_token(subject=user.email)
    new_refresh_token = create_refresh_token(subject=user.email)
    
    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current user information.
    
    Requires authentication.
    
    Args:
        current_user: Current authenticated user
    
    Returns:
        UserResponse: Current user data
    """
    return current_user


@router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Change current user's password.
    
    Requires authentication.
    
    Args:
        password_data: Current and new passwords
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        dict: Success message
    
    Raises:
        HTTPException: If current password is incorrect
    """
    # Verify current password
    if not verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password"
        )
    
    # Update password
    user_crud.update_user_password(
        db,
        user=current_user,
        new_password=password_data.new_password
    )
    
    return {"message": "Password updated successfully"}


@router.post("/deactivate")
async def deactivate_account(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Deactivate current user's account.
    
    Requires authentication.
    
    Args:
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        dict: Success message
    """
    user_crud.deactivate_user(db, user=current_user)
    
    return {"message": "Account deactivated successfully"}


@router.get("/test-token")
async def test_token(current_user: User = Depends(get_current_user)):
    """
    Test if the authentication token is valid.
    
    Requires authentication.
    
    Args:
        current_user: Current authenticated user
    
    Returns:
        dict: User email
    """
    return {"email": current_user.email}