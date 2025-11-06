"""
Authentication Schemas

Pydantic models for request/response validation in authentication endpoints.
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional


# ============================================
# USER SCHEMAS
# ============================================

class UserBase(BaseModel):
    """Base user schema with common fields."""
    email: EmailStr = Field(..., description="User email address")
    username: str = Field(..., min_length=3, max_length=50, description="Username")


class UserCreate(UserBase):
    """Schema for user registration."""
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="Password (min 8 characters)"
    )
    
    @validator("password")
    def validate_password_strength(cls, v):
        """Ensure password meets security requirements."""
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isupper() for char in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in v):
            raise ValueError("Password must contain at least one lowercase letter")
        return v
    
    @validator("username")
    def validate_username(cls, v):
        """Ensure username is alphanumeric."""
        if not v.isalnum():
            raise ValueError("Username must be alphanumeric (no spaces or special characters)")
        return v


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class UserResponse(UserBase):
    """Schema for user response (public info only)."""
    id: int
    is_active: bool
    is_superuser: bool
    
    class Config:
        from_attributes = True  # Pydantic v2 (was orm_mode in v1)


class UserInDB(UserResponse):
    """Schema for user in database (includes sensitive fields)."""
    hashed_password: str


# ============================================
# TOKEN SCHEMAS
# ============================================

class Token(BaseModel):
    """Schema for token response."""
    access_token: str = Field(..., description="JWT access token")
    refresh_token: Optional[str] = Field(None, description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")


class TokenPayload(BaseModel):
    """Schema for decoded token payload."""
    sub: Optional[str] = None  # Subject (user_id or email)
    exp: Optional[int] = None  # Expiration timestamp
    type: Optional[str] = None  # Token type (access/refresh)


class RefreshTokenRequest(BaseModel):
    """Schema for refresh token request."""
    refresh_token: str = Field(..., description="Refresh token")


# ============================================
# PASSWORD SCHEMAS
# ============================================

class PasswordChange(BaseModel):
    """Schema for password change."""
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="New password"
    )
    
    @validator("new_password")
    def validate_new_password(cls, v, values):
        """Ensure new password is different and strong."""
        if "current_password" in values and v == values["current_password"]:
            raise ValueError("New password must be different from current password")
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isupper() for char in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in v):
            raise ValueError("Password must contain at least one lowercase letter")
        return v


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr = Field(..., description="Email address")


class PasswordReset(BaseModel):
    """Schema for password reset (with token)."""
    token: str = Field(..., description="Password reset token")
    new_password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="New password"
    )