"""
FastAPI dependencies for authentication and authorization.
"""

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import logging

from app.db.session import get_db
from app.models.user import User, UserRole
from app.security.auth import verify_token
from app.core.config import settings

logger = logging.getLogger(__name__)

# HTTP Bearer token security scheme
security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Get the current authenticated user from JWT token.
    
    Args:
        credentials: HTTP Bearer credentials
        db: Database session
        
    Returns:
        The authenticated user
        
    Raises:
        HTTPException: If authentication fails
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    payload = verify_token(token, token_type="access")
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user from database
    from sqlalchemy import select
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """
    Get the current user if authenticated, otherwise return None.
    
    Useful for endpoints that work differently for authenticated vs anonymous users.
    """
    try:
        return await get_current_user(credentials, db)
    except HTTPException:
        return None


async def require_role(required_role: UserRole):
    """
    Dependency factory to require a specific user role.
    
    Usage:
        @router.get("/admin")
        async def admin_endpoint(user: User = Depends(require_role(UserRole.ADMIN))):
            ...
    """
    async def role_checker(
        user: User = Depends(get_current_user)
    ) -> User:
        role_hierarchy = {
            UserRole.FREE: 0,
            UserRole.STARTER: 1,
            UserRole.PROFESSIONAL: 2,
            UserRole.BUSINESS: 3,
            UserRole.ENTERPRISE: 4,
            UserRole.ADMIN: 5,
        }
        
        user_level = role_hierarchy.get(user.role, 0)
        required_level = role_hierarchy.get(required_role, 0)
        
        if user_level < required_level:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required role: {required_role.value}",
            )
        
        return user
    
    return role_checker


async def require_admin(
    user: User = Depends(get_current_user)
) -> User:
    """Require admin role."""
    if user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return user


async def require_verified(
    user: User = Depends(get_current_user)
) -> User:
    """Require verified email."""
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email verification required",
        )
    return user


async def require_subscription(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Require active paid subscription."""
    if user.role == UserRole.FREE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Active subscription required",
        )
    return user


async def get_api_key_user(
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """
    Authenticate user via API key header.
    
    Looks for X-API-Key header.
    """
    api_key = request.headers.get("X-API-Key")
    
    if not api_key:
        return None
    
    # TODO: Implement API key lookup in database
    # For now, return None to fall back to JWT auth
    return None


async def get_current_user_with_api_key(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Get current user via API key or JWT token.
    
    Tries API key first, then falls back to JWT.
    """
    # Try API key authentication
    api_user = await get_api_key_user(request, db)
    if api_user:
        return api_user
    
    # Fall back to JWT authentication
    return await get_current_user(credentials, db)


async def check_rate_limit(
    user: User = Depends(get_current_user),
    request: Request = None
) -> User:
    """
    Check rate limits for the current user.
    
    TODO: Implement Redis-based rate limiting.
    """
    # Placeholder for rate limiting logic
    return user


async def get_client_ip(request: Request) -> str:
    """
    Get client IP address from request.
    
    Handles proxied requests (Cloudflare, nginx, etc.).
    """
    # Check for Cloudflare IP
    cf_ip = request.headers.get("CF-Connecting-IP")
    if cf_ip:
        return cf_ip
    
    # Check for X-Forwarded-For
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # Take the first IP in the chain
        return forwarded_for.split(",")[0].strip()
    
    # Check for X-Real-IP
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip
    
    # Fall back to direct client IP
    if request.client:
        return request.client.host
    
    return "unknown"
