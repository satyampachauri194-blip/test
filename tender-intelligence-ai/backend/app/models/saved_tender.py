"""
Saved Tender model for user bookmarks.
"""

from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP, JSONB
from sqlalchemy.sql import func
import uuid

from app.db.session import Base


class SavedTender(Base):
    """
    SavedTender model for user bookmarked tenders.
    
    Allows users to save tenders with notes and tags for easy reference.
    """
    
    __tablename__ = "saved_tenders"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign keys
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    tender_id = Column(UUID(as_uuid=True), ForeignKey("tenders.id"), nullable=False, index=True)
    
    # User annotations
    notes = Column(Text, nullable=True)
    tags = Column(JSONB, default=list, nullable=True)  # Custom tags added by user
    
    # Status
    is_archived = Column(Boolean, default=False, nullable=True)
    
    # Reminders
    reminder_enabled = Column(Boolean, default=True, nullable=True)
    reminder_days_before = Column(Integer, default=3, nullable=True)  # Days before closing date
    
    # Statistics
    view_count = Column(Integer, default=0, nullable=True)
    last_viewed_at = Column(TIMESTAMP(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self) -> str:
        return f"<SavedTender {self.user_id}: {self.tender_id}>"
