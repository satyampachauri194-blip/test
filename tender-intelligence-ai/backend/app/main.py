"""
FastAPI application factory and configuration.
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import time

from app.core.config import settings
from app.db.session import init_db, close_db
from app.api.v1.router import api_router

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting Tender Intelligence AI API...")
    
    try:
        # Initialize database
        await init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise
    
    # Initialize Elasticsearch
    # TODO: Add ES initialization
    
    # Initialize Redis
    # TODO: Add Redis initialization
    
    logger.info(f"{settings.APP_NAME} v{settings.APP_VERSION} started successfully")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Tender Intelligence AI API...")
    
    await close_db()
    
    # Close other connections
    # TODO: Close ES, Redis connections
    
    logger.info("Shutdown complete")


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        Configured FastAPI application instance
    """
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="""
## Tender Intelligence AI API

Enterprise-grade SaaS platform for Indian Government Tender & Procurement ecosystem.

### Features

* **Tender Search**: Advanced search with filters for location, category, value, dates
* **AI Analysis**: Automatic extraction and analysis of tender documents
* **Smart Alerts**: Real-time notifications for matching opportunities
* **Subscription Plans**: Multiple tiers from Free to Enterprise
* **Secure Authentication**: JWT-based auth with OAuth support

### Authentication

Most endpoints require authentication via Bearer token:
```
Authorization: Bearer <your_token>
```

API key authentication is also supported:
```
X-API-Key: <your_api_key>
```
        """,
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        openapi_url="/openapi.json" if settings.DEBUG else None,
        lifespan=lifespan,
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )
    
    # Request timing middleware
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000  # milliseconds
        response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
        return response
    
    # Security headers middleware
    @app.middleware("http")
    async def add_security_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response
    
    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "Internal server error",
                "type": type(exc).__name__,
            } if settings.DEBUG else {"detail": "Internal server error"}
        )
    
    # Include API router
    app.include_router(api_router, prefix=settings.API_PREFIX)
    
    # Health check endpoint
    @app.get("/health", tags=["Health"])
    async def health_check():
        """
        Health check endpoint for load balancers and monitoring.
        """
        return {
            "status": "healthy",
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
        }
    
    # Root endpoint
    @app.get("/", tags=["Root"])
    async def root():
        """
        Root endpoint with API information.
        """
        return {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "description": "Enterprise-grade SaaS platform for Indian Government Tenders",
            "docs": "/docs" if settings.DEBUG else None,
            "health": "/health",
            "api": settings.API_PREFIX,
        }
    
    return app


# Create application instance
app = create_application()
