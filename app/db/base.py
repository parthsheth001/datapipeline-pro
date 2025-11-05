"""
Database Base Configuration

This module sets up the base SQLAlchemy configuration that all models inherit from.
"""

from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

# Naming convention for constraints (for better migration names)
convention = {
    "ix": "ix_%(column_0_label)s",  # Index
    "uq": "uq_%(table_name)s_%(column_0_name)s",  # Unique constraint
    "ck": "ck_%(table_name)s_%(constraint_name)s",  # Check constraint
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",  # Foreign key
    "pk": "pk_%(table_name)s"  # Primary key
}

metadata = MetaData(naming_convention=convention)

# Base class for all database models
Base = declarative_base(metadata=metadata)