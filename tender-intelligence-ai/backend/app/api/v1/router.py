"""
API Router for v1 endpoints.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    users,
    tenders,
    search,
    alerts,
    subscriptions,
    payments,
    health,
)

# Create main API router for v1
api_router = APIRouter()

# Include endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(tenders.router, prefix="/tenders", tags=["Tenders"])
api_router.include_router(search.router, prefix="/search", tags=["Search"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["Alerts"])
api_router.include_router(subscriptions.router, prefix="/subscriptions", tags=["Subscriptions"])
api_router.include_router(payments.router, prefix="/payments", tags=["Payments"])
api_router.include_router(health.router, prefix="/health", tags=["Health"])


@api_router.get("/", tags=["Root"])
async def api_root():
    """
    API v1 root endpoint.
    """
    return {
        "message": "Welcome to Tender Intelligence AI API v1",
        "version": "1.0.0",
        "endpoints": {
            "auth": "/api/v1/auth",
            "users": "/api/v1/users",
            "tenders": "/api/v1/tenders",
            "search": "/api/v1/search",
            "alerts": "/api/v1/alerts",
            "subscriptions": "/api/v1/subscriptions",
            "payments": "/api/v1/payments",
            "health": "/api/v1/health",
        }
    }
