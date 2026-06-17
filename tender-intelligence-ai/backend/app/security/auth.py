"""
Security utilities for authentication and authorization.
"""

from datetime import datetime, timedelta
from typing import Optional, Union, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    
    Args:
        plain_password: The plain text password
        hashed_password: The hashed password to compare against
        
    Returns:
        True if passwords match, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password: The plain text password to hash
        
    Returns:
        The hashed password
    """
    return pwd_context.hash(password)


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: The data to encode in the token
        expires_delta: Optional custom expiration time
        
    Returns:
        The encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    })
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt


def create_refresh_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT refresh token.
    
    Args:
        data: The data to encode in the token
        expires_delta: Optional custom expiration time
        
    Returns:
        The encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    })
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    """
    Decode and validate a JWT token.
    
    Args:
        token: The JWT token to decode
        
    Returns:
        The decoded token payload or None if invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError as e:
        logger.error(f"Token decoding error: {e}")
        return None


def verify_token(token: str, token_type: str = "access") -> Optional[dict]:
    """
    Verify a JWT token and check its type.
    
    Args:
        token: The JWT token to verify
        token_type: Expected token type ("access" or "refresh")
        
    Returns:
        The decoded token payload or None if invalid
    """
    payload = decode_token(token)
    
    if not payload:
        return None
    
    # Check token type
    if payload.get("type") != token_type:
        logger.warning(f"Invalid token type: expected {token_type}, got {payload.get('type')}")
        return None
    
    # Check expiration
    exp = payload.get("exp")
    if exp and datetime.utcnow() > datetime.fromtimestamp(exp):
        logger.warning("Token has expired")
        return None
    
    return payload


def create_verification_token(email: str) -> str:
    """
    Create an email verification token.
    
    Args:
        email: The email to verify
        
    Returns:
        The verification token
    """
    return create_access_token(
        data={"email": email, "type": "verification"},
        expires_delta=timedelta(hours=24)
    )


def create_password_reset_token(email: str) -> str:
    """
    Create a password reset token.
    
    Args:
        email: The email for password reset
        
    Returns:
        The password reset token
    """
    return create_access_token(
        data={"email": email, "type": "password_reset"},
        expires_delta=timedelta(hours=1)
    )


def generate_api_key() -> str:
    """
    Generate a secure API key.
    
    Returns:
        A random API key string
    """
    import secrets
    return f"tia_{secrets.token_urlsafe(32)}"
