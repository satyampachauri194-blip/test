"""
Audit Log model for security and compliance.
"""

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP, JSONB, INET
from sqlalchemy.sql import func
import uuid

from app.db.session import Base


class AuditLog(Base):
    """
    AuditLog model for tracking all user actions and system events.
    
    Essential for security, compliance, debugging, and analytics.
    """
    
    __tablename__ = "audit_logs"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Actor
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)
    user_email = Column(VARCHAR(255), nullable=True, index=True)
    
    # Action details
    action = Column(VARCHAR(100), nullable=False, index=True)  # e.g., "LOGIN", "SEARCH", "DOWNLOAD_PDF"
    resource_type = Column(VARCHAR(100), nullable=True, index=True)  # e.g., "tender", "user", "subscription"
    resource_id = Column(UUID(as_uuid=True), nullable=True)
    
    # Request info
    ip_address = Column(INET, nullable=True)
    user_agent = Column(Text, nullable=True)
    referer = Column(Text, nullable=True)
    
    # Location (if available)
    country = Column(VARCHAR(2), nullable=True)
    city = Column(VARCHAR(100), nullable=True)
    
    # Additional context
    metadata = Column(JSONB, default=dict, nullable=True)
    
    # Outcome
    status_code = Column(Integer, nullable=True)
    error_message = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True)
    
    def __repr__(self) -> str:
        return f"<AuditLog {self.action} by {self.user_email or 'anonymous'}>"
    
    @classmethod
    def get_action_category(cls, action: str) -> str:
        """Categorize audit actions for reporting."""
        auth_actions = ["LOGIN", "LOGOUT", "REGISTER", "VERIFY_EMAIL", "RESET_PASSWORD"]
        tender_actions = ["VIEW_TENDER", "DOWNLOAD_PDF", "SAVE_TENDER", "EXPORT_TENDER"]
        search_actions = ["SEARCH", "ADVANCED_SEARCH", "FILTER_APPLIED"]
        subscription_actions = ["SUBSCRIBE", "CANCEL_SUBSCRIPTION", "UPGRADE", "DOWNGRADE"]
        alert_actions = ["CREATE_ALERT", "UPDATE_ALERT", "DELETE_ALERT", "TRIGGER_ALERT"]
        admin_actions = ["USER_MANAGEMENT", "SYSTEM_CONFIG", "DATA_EXPORT", "SCRAPER_CONTROL"]
        
        if action in auth_actions:
            return "authentication"
        elif action in tender_actions:
            return "tender_interaction"
        elif action in search_actions:
            return "search"
        elif action in subscription_actions:
            return "subscription"
        elif action in alert_actions:
            return "alerts"
        elif action in admin_actions:
            return "admin"
        else:
            return "other"
