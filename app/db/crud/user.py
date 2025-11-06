"""
User CRUD Operations

Database operations for user management.
"""

from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.db.models.user import User
from app.schemas.auth import UserCreate
from app.core.security import get_password_hash, verify_password


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """
    Get user by ID.
    
    Args:
        db: Database session
        user_id: User ID
    
    Returns:
        User object if found, None otherwise
    """
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Get user by email address.
    
    Args:
        db: Database session
        email: User email
    
    Returns:
        User object if found, None otherwise
    """
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """
    Get user by username.
    
    Args:
        db: Database session
        username: Username
    
    Returns:
        User object if found, None otherwise
    """
    return db.query(User).filter(User.username == username).first()


def get_user_by_email_or_username(
    db: Session,
    email: str,
    username: str
) -> Optional[User]:
    """
    Check if user exists with given email or username.
    
    Args:
        db: Database session
        email: Email to check
        username: Username to check
    
    Returns:
        User object if found, None otherwise
    """
    return db.query(User).filter(
        or_(User.email == email, User.username == username)
    ).first()


def create_user(db: Session, user_in: UserCreate) -> User:
    """
    Create a new user.
    
    Args:
        db: Database session
        user_in: User creation schema
    
    Returns:
        Created user object
    """
    hashed_password = get_password_hash(user_in.password)
    
    db_user = User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=hashed_password,
        is_active=True,
        is_superuser=False
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


def authenticate_user(
    db: Session,
    email: str,
    password: str
) -> Optional[User]:
    """
    Authenticate a user by email and password.
    
    Args:
        db: Database session
        email: User email
        password: Plain text password
    
    Returns:
        User object if authentication successful, None otherwise
    """
    user = get_user_by_email(db, email)
    
    if not user:
        return None
    
    if not verify_password(password, user.hashed_password):
        return None
    
    if not user.is_active:
        return None
    
    return user


def update_user_password(
    db: Session,
    user: User,
    new_password: str
) -> User:
    """
    Update user's password.
    
    Args:
        db: Database session
        user: User object
        new_password: New plain text password
    
    Returns:
        Updated user object
    """
    user.hashed_password = get_password_hash(new_password)
    db.commit()
    db.refresh(user)
    
    return user


def deactivate_user(db: Session, user: User) -> User:
    """
    Deactivate a user account.
    
    Args:
        db: Database session
        user: User object
    
    Returns:
        Updated user object
    """
    user.is_active = False
    db.commit()
    db.refresh(user)
    
    return user


def activate_user(db: Session, user: User) -> User:
    """
    Activate a user account.
    
    Args:
        db: Database session
        user: User object
    
    Returns:
        Updated user object
    """
    user.is_active = True
    db.commit()
    db.refresh(user)
    
    return user