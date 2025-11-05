"""
Database Models Package

Import all models here for easy access and Alembic auto-detection.
"""

from app.db.models.user import User

# Export all models
__all__ = ["User"]