"""
Database Session Management

This module handles database connections, sessions, and engine configuration.
Supports both sync and async operations.
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from typing import Generator
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

# ============================================
# SYNC ENGINE & SESSION (for migrations, scripts)
# ============================================

# Create synchronous database engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=settings.DB_POOL_RECYCLE,
    echo=settings.DB_ECHO,  # Log SQL queries if True
)

# Session factory for creating database sessions
SessionLocal = sessionmaker(
    autocommit=False,  # Don't auto-commit (explicit commits)
    autoflush=False,   # Don't auto-flush (explicit flushes)
    bind=engine,
    class_=Session,
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get database session.
    
    Usage in FastAPI:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            users = db.query(User).all()
            return users
    
    Yields:
        Session: Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================
# ASYNC ENGINE & SESSION (for FastAPI endpoints)
# ============================================

# Create asynchronous database engine
async_engine = create_async_engine(
    settings.database_url_async,  # postgresql+asyncpg://...
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_pre_ping=True,
    pool_recycle=settings.DB_POOL_RECYCLE,
    echo=settings.DB_ECHO,
)

# Async session factory
AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_async_db() -> AsyncSession:
    """
    Async dependency function to get database session.
    
    Usage in FastAPI:
        @app.get("/users")
        async def get_users(db: AsyncSession = Depends(get_async_db)):
            result = await db.execute(select(User))
            users = result.scalars().all()
            return users
    
    Yields:
        AsyncSession: Async database session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# ============================================
# DATABASE UTILITIES
# ============================================

def init_db():
    """
    Initialize database - create all tables.
    Only use for development/testing!
    In production, use Alembic migrations.
    """
    from app.db.base import Base
    
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully!")


def check_db_connection() -> bool:
    """
    Check if database connection is working.
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        # Use context manager for automatic connection cleanup
        with engine.connect() as connection:
            # Execute simple query using text() for raw SQL
            result = connection.execute(text("SELECT 1"))
            result.fetchone()  # Actually fetch the result
        
        logger.info("✅ Database connection successful")
        return True
        
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        logger.error(f"Database URL: {settings.DATABASE_URL.split('@')[1]}")  # Don't log password
        return False

"""
### **Explanation:**

**`create_engine()`** - Creates database engine
- `pool_size` - Number of connections to keep open
- `max_overflow` - Extra connections allowed when pool is full
- `pool_pre_ping` - Test connection before using (catches stale connections)
- `pool_recycle` - Recycle connections after X seconds (prevents timeouts)
- `echo` - Log all SQL (useful for debugging)

**`sessionmaker()`** - Factory for creating sessions
- `autocommit=False` - Manual transaction control
- `autoflush=False` - Manual flush control
- `bind=engine` - Connect to this engine

**`get_db()`** - Dependency injection for FastAPI
- Creates session
- Yields it to route
- Automatically closes after request

**Why two engines (sync/async)?**
- **Sync** - For migrations, scripts, simple operations
- **Async** - For FastAPI endpoints (better performance)

**Connection pooling:**

Request 1 → Get connection from pool → Use it → Return to pool
Request 2 → Reuse same connection → Much faster!
"""