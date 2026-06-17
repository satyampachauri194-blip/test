"""
Alert model for user notifications.
"""

from sqlalchemy import Column, String, Boolean, DateTime, Enum as SQLEnum, ForeignKey, VARCHAR, Text
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP, JSONB
from sqlalchemy.sql import func
import uuid
import enum

from app.db.session import Base


class AlertFrequency(enum.Enum):
    """Alert delivery frequency."""
    INSTANT = "instant"
    DAILY = "daily"
    WEEKLY = "weekly"


class Alert(Base):
    """
    Alert model for user-defined tender notifications.
    
    Users can create custom alerts based on keywords and filters,
    and receive notifications via multiple channels.
    """
    
    __tablename__ = "alerts"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign key to user
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # Alert configuration
    name = Column(VARCHAR(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Search criteria
    keywords = Column(JSONB, default=list, nullable=True)  # List of keywords to match
    filters = Column(JSONB, default=dict, nullable=True)  # Advanced filters
    
    # Filter options stored in JSONB:
    # {
    #     "states": ["Delhi", "Maharashtra"],
    #     "departments": ["Railways", "PWD"],
    #     "categories": ["Services", "Works"],
    #     "min_bid_value": 100000,
    #     "max_bid_value": 10000000,
    #     "procurement_types": ["goods", "services"],
    #     "tender_types": ["open", "ge_m"],
    #     "exclude_keywords": ["cancelled", "corrigendum"],
    #     "closing_within_days": 30,
    #     "published_within_days": 7,
    # }
    
    # Delivery settings
    frequency = Column(SQLEnum(AlertFrequency), default=AlertFrequency.DAILY, nullable=False)
    channels = Column(JSONB, default=list, nullable=True)  # ["email", "sms", "whatsapp", "telegram"]
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    last_triggered_at = Column(TIMESTAMP(timezone=True), nullable=True)
    last_sent_at = Column(TIMESTAMP(timezone=True), nullable=True)
    
    # Statistics
    trigger_count = Column(Integer, default=0, nullable=True)
    match_count = Column(Integer, default=0, nullable=True)
    click_count = Column(Integer, default=0, nullable=True)
    
    # Timestamps
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self) -> str:
        return f"<Alert {self.name}>"
    
    @property
    def is_enabled(self) -> bool:
        """Check if alert is currently enabled."""
        return self.is_active
    
    def get_filter_summary(self) -> str:
        """Get human-readable summary of alert filters."""
        if not self.filters:
            return "All tenders"
        
        parts = []
        if self.filters.get("states"):
            parts.append(f"States: {', '.join(self.filters['states'])}")
        if self.filters.get("departments"):
            parts.append(f"Departments: {', '.join(self.filters['departments'])}")
        if self.filters.get("categories"):
            parts.append(f"Categories: {', '.join(self.filters['categories'])}")
        if self.filters.get("min_bid_value"):
            parts.append(f"Min Value: ₹{self.filters['min_bid_value']:,}")
        if self.filters.get("max_bid_value"):
            parts.append(f"Max Value: ₹{self.filters['max_bid_value']:,}")
        if self.filters.get("closing_within_days"):
            parts.append(f"Closing within {self.filters['closing_within_days']} days")
        
        return "; ".join(parts) if parts else "All tenders"
