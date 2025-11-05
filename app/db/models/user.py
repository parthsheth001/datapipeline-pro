"""
User Database Model

Represents the users table in the database.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class User(Base):
    """
    User model for authentication and user management.
    
    Attributes:
        id: Primary key
        email: User email (unique)
        username: User username (unique)
        hashed_password: Bcrypt hashed password
        is_active: Account active status
        is_superuser: Admin privileges
        created_at: Account creation timestamp
        updated_at: Last update timestamp
    """
    
    __tablename__ = "users"
    
    # Primary Key
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
        comment="User ID"
    )
    
    # Email (unique, required)
    email = Column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
        comment="User email address"
    )
    
    # Username (unique, required)
    username = Column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
        comment="Username for login"
    )
    
    # Password (hashed, required)
    hashed_password = Column(
        String(255),
        nullable=False,
        comment="Bcrypt hashed password"
    )
    
    # Status flags
    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
        comment="Account active status"
    )
    
    is_superuser = Column(
        Boolean,
        default=False,
        nullable=False,
        comment="Admin privileges flag"
    )
    
    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Account creation timestamp"
    )
    
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Last update timestamp"
    )
    
    def __repr__(self) -> str:
        """String representation of User object."""
        return f"<User(id={self.id}, email='{self.email}', username='{self.username}')>"
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        return self.username