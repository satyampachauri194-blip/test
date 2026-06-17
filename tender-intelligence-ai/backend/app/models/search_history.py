"""
Search History model for tracking user searches.
"""

from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP, JSONB
from sqlalchemy.sql import func
import uuid

from app.db.session import Base


class SearchHistory(Base):
    """
    SearchHistory model for tracking user search activity.
    
    Used for analytics, suggestions, and improving search relevance.
    """
    
    __tablename__ = "search_history"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign key to user
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)  # Nullable for anonymous searches
    
    # Search details
    query = Column(Text, nullable=False)
    filters = Column(JSONB, default=dict, nullable=True)
    
    # Results
    results_count = Column(Integer, nullable=True)
    clicked_tender_ids = Column(JSONB, default=list, nullable=True)  # Tenders user clicked on
    
    # Session info
    session_id = Column(VARCHAR(100), nullable=True, index=True)
    ip_address = Column(VARCHAR(45), nullable=True)  # IPv6 compatible
    user_agent = Column(String, nullable=True)
    
    # Performance
    response_time_ms = Column(Integer, nullable=True)
    
    # Timestamps
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, index=True)
    
    def __repr__(self) -> str:
        return f"<SearchHistory {self.query[:50]}>"
