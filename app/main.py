"""
DataPipeline Pro - Main Application Entry Point

This is the core FastAPI application with all middleware and routing configuration.
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import time
import logging

from app.core.config import get_settings
from app.api.v1.router import api_router
from app.db.session import check_db_connection

# Get settings instance
settings = get_settings()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Real-time Data Processing & Analytics Platform built with FastAPI, Kafka, and Airflow",
    version=settings.API_VERSION,
    debug=settings.DEBUG,
    docs_url="/docs" if settings.DEBUG else None,  # Disable docs in production
    redoc_url="/redoc" if settings.DEBUG else None,
)

# Include API v1 routes
app.include_router(
    api_router,
    prefix=settings.API_PREFIX
)

@app.on_event("startup")
async def startup_event():
    """Execute on application startup."""
    logger.info("=" * 60)
    logger.info(f"Starting {settings.APP_NAME}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug Mode: {settings.DEBUG}")
    logger.info(f"API Version: {settings.API_VERSION}")
    logger.info("=" * 60)
    
    # Check database connection
    logger.info("Checking database connection...")
    if check_db_connection():
        logger.info("✅ Database connected successfully")
    else:
        logger.error("❌ Database connection failed!")
    
    if settings.is_development:
        logger.info("Running in DEVELOPMENT mode")

# ============================================
# MIDDLEWARE
# ============================================

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted Host Middleware (security)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)


# Custom middleware for request logging and timing
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Log all requests and measure response time.
    """
    start_time = time.time()
    
    # Log incoming request
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    
    # Process request
    response = await call_next(request)
    
    # Calculate response time
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    # Log response
    logger.info(
        f"Completed: {request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.4f}s"
    )
    
    return response


# ============================================
# EVENT HANDLERS
# ============================================

@app.on_event("startup")
async def startup_event():
    """
    Execute on application startup.
    """
    logger.info("=" * 60)
    logger.info(f"Starting {settings.APP_NAME}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug Mode: {settings.DEBUG}")
    logger.info(f"API Version: {settings.API_VERSION}")
    logger.info("=" * 60)
    
    # Future: Initialize database connections, Redis, Kafka, etc.
    if settings.is_development:
        logger.info("Running in DEVELOPMENT mode")
    elif settings.is_production:
        logger.warning("Running in PRODUCTION mode")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Execute on application shutdown.
    """
    logger.info("=" * 60)
    logger.info(f"Shutting down {settings.APP_NAME}")
    logger.info("=" * 60)
    
    # Future: Close database connections, Redis, Kafka, etc.


# ============================================
# EXCEPTION HANDLERS
# ============================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for unhandled errors.
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": str(exc) if settings.DEBUG else "An unexpected error occurred",
            "path": request.url.path,
        }
    )


# ============================================
# ROUTES
# ============================================

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint - basic API information.
    """
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "status": "running",
        "version": settings.API_VERSION,
        "environment": settings.ENVIRONMENT,
        "docs": "/docs" if settings.DEBUG else "Documentation disabled in production",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.API_VERSION,
        "environment": settings.ENVIRONMENT,
    }


@app.get("/info", tags=["Info"])
async def app_info():
    """
    Application information endpoint.
    Shows non-sensitive configuration details.
    """
    return {
        "application": {
            "name": settings.APP_NAME,
            "version": settings.API_VERSION,
            "environment": settings.ENVIRONMENT,
            "debug": settings.DEBUG,
        },
        "api": {
            "prefix": settings.API_PREFIX,
            "rate_limit": f"{settings.RATE_LIMIT_PER_MINUTE}/min",
        },
        "features": {
            "metrics_enabled": settings.ENABLE_METRICS,
            "kafka_enabled": bool(settings.KAFKA_BOOTSTRAP_SERVERS),
            "aws_enabled": bool(settings.AWS_ACCESS_KEY_ID),
        }
    }


@app.get("/config/test", tags=["Config"])
async def test_config():
    """
    Test configuration endpoint - only available in development.
    Shows how to access settings in routes.
    """
    if not settings.is_development:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"error": "This endpoint is only available in development mode"}
        )
    
    return {
        "message": "Configuration test endpoint",
        "database": {
            "pool_size": settings.DB_POOL_SIZE,
            "echo": settings.DB_ECHO,
        },
        "redis": {
            "max_connections": settings.REDIS_MAX_CONNECTIONS,
        },
        "security": {
            "algorithm": settings.ALGORITHM,
            "token_expire": f"{settings.ACCESS_TOKEN_EXPIRE_MINUTES} minutes",
            "secret_key_length": len(settings.SECRET_KEY),
        }
    }


# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,  # Auto-reload in debug mode
        log_level=settings.LOG_LEVEL.lower(),
    )