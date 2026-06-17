"""
User model for authentication and authorization.
"""

from sqlalchemy import Column, String, Boolean, DateTime, Enum as SQLEnum, VARCHAR
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy.sql import func
import uuid
import enum

from app.db.session import Base


class UserRole(enum.Enum):
    """User role enumeration for RBAC."""
    FREE = "free"
    STARTER = "starter"
    PROFESSIONAL = "professional"
    BUSINESS = "business"
    ENTERPRISE = "enterprise"
    ADMIN = "admin"


class User(Base):
    """
    User model representing platform users.
    
    Supports multiple subscription tiers and role-based access control.
    """
    
    __tablename__ = "users"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Authentication
    email = Column(VARCHAR(255), unique=True, nullable=False, index=True)
    password_hash = Column(VARCHAR(255), nullable=True)  # Nullable for OAuth-only users
    phone = Column(VARCHAR(20), nullable=True)
    
    # Profile information
    first_name = Column(VARCHAR(100), nullable=True)
    last_name = Column(VARCHAR(100), nullable=True)
    company_name = Column(VARCHAR(255), nullable=True)
    gst_number = Column(VARCHAR(20), nullable=True)
    pan_number = Column(VARCHAR(10), nullable=True)
    
    # Role and permissions
    role = Column(
        SQLEnum(UserRole),
        default=UserRole.FREE,
        nullable=False,
        index=True
    )
    
    # Account status
    is_verified = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    last_login = Column(TIMESTAMP(timezone=True), nullable=True)
    email_verified_at = Column(TIMESTAMP(timezone=True), nullable=True)
    
    # OAuth providers
    google_id = Column(VARCHAR(255), unique=True, nullable=True)
    github_id = Column(VARCHAR(255), unique=True, nullable=True)
    
    # Preferences
    timezone = Column(VARCHAR(50), default="Asia/Kolkata", nullable=True)
    language = Column(VARCHAR(10), default="en", nullable=True)
    notification_enabled = Column(Boolean, default=True, nullable=True)
    
    def __repr__(self) -> str:
        return f"<User {self.email}>"
    
    @property
    def full_name(self) -> str:
        """Get user's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.email:
            return self.email.split("@")[0]
        return "User"
    
    @property
    def is_admin(self) -> bool:
        """Check if user has admin privileges."""
        return self.role == UserRole.ADMIN
    
    @property
    def is_paid(self) -> bool:
        """Check if user has a paid subscription."""
        return self.role not in [UserRole.FREE]
    
    def get_plan_limits(self) -> dict:
        """Get usage limits based on user's plan."""
        limits = {
            UserRole.FREE: {
                "daily_searches": 10,
                "pdf_downloads": 0,
                "ai_analyses": 0,
                "saved_tenders": 5,
                "alerts": 1,
                "team_members": 1,
                "api_access": False,
                "historical_data_days": 7,
                "export_formats": [],
            },
            UserRole.STARTER: {
                "daily_searches": 50,
                "pdf_downloads": 5,
                "ai_analyses": 3,
                "saved_tenders": 25,
                "alerts": 3,
                "team_members": 2,
                "api_access": False,
                "historical_data_days": 30,
                "export_formats": ["csv"],
            },
            UserRole.PROFESSIONAL: {
                "daily_searches": 200,
                "pdf_downloads": 25,
                "ai_analyses": 15,
                "saved_tenders": 100,
                "alerts": 10,
                "team_members": 5,
                "api_access": True,
                "historical_data_days": 90,
                "export_formats": ["csv", "excel"],
            },
            UserRole.BUSINESS: {
                "daily_searches": 1000,
                "pdf_downloads": 100,
                "ai_analyses": 50,
                "saved_tenders": 500,
                "alerts": 25,
                "team_members": 20,
                "api_access": True,
                "historical_data_days": 365,
                "export_formats": ["csv", "excel", "json", "pdf"],
            },
            UserRole.ENTERPRISE: {
                "daily_searches": -1,  # Unlimited
                "pdf_downloads": -1,
                "ai_analyses": -1,
                "saved_tenders": -1,
                "alerts": -1,
                "team_members": 100,
                "api_access": True,
                "historical_data_days": 1825,  # 5 years
                "export_formats": ["csv", "excel", "json", "pdf", "api"],
            },
            UserRole.ADMIN: {
                "daily_searches": -1,
                "pdf_downloads": -1,
                "ai_analyses": -1,
                "saved_tenders": -1,
                "alerts": -1,
                "team_members": -1,
                "api_access": True,
                "historical_data_days": -1,
                "export_formats": ["csv", "excel", "json", "pdf", "api"],
            },
        }
        return limits.get(self.role, limits[UserRole.FREE])
