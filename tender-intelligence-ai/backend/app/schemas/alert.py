"""
Alert schemas for notification management.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import uuid


class AlertFrequency(str, Enum):
    """Alert delivery frequency."""
    INSTANT = "instant"
    DAILY = "daily"
    WEEKLY = "weekly"


class NotificationChannel(str, Enum):
    """Notification channel types."""
    EMAIL = "email"
    SMS = "sms"
    WHATSAPP = "whatsapp"
    TELEGRAM = "telegram"
    PUSH = "push"


class AlertFilters(BaseModel):
    """Schema for alert filters configuration."""
    
    states: Optional[List[str]] = None
    districts: Optional[List[str]] = None
    departments: Optional[List[str]] = None
    categories: Optional[List[str]] = None
    min_bid_value: Optional[float] = None
    max_bid_value: Optional[float] = None
    procurement_types: Optional[List[str]] = None
    tender_types: Optional[List[str]] = None
    exclude_keywords: Optional[List[str]] = None
    closing_within_days: Optional[int] = Field(None, ge=1, le=365)
    published_within_days: Optional[int] = Field(None, ge=1, le=90)


class AlertCreate(BaseModel):
    """Schema for creating a new alert."""
    
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=500)
    keywords: List[str] = Field(..., min_length=1)
    filters: Optional[AlertFilters] = None
    frequency: AlertFrequency = AlertFrequency.DAILY
    channels: List[NotificationChannel] = Field(default=[NotificationChannel.EMAIL])
    is_active: bool = True
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Housekeeping Services in Delhi",
                "description": "Alerts for housekeeping tenders in NCR region",
                "keywords": ["housekeeping", "facility management", "cleaning services"],
                "filters": {
                    "states": ["Delhi", "Haryana", "Uttar Pradesh"],
                    "min_bid_value": 100000,
                    "closing_within_days": 30
                },
                "frequency": "daily",
                "channels": ["email", "whatsapp"]
            }
        }


class AlertUpdate(BaseModel):
    """Schema for updating an existing alert."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=500)
    keywords: Optional[List[str]] = None
    filters: Optional[AlertFilters] = None
    frequency: Optional[AlertFrequency] = None
    channels: Optional[List[NotificationChannel]] = None
    is_active: Optional[bool] = None


class AlertResponse(BaseModel):
    """Schema for alert response."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    user_id: uuid.UUID
    name: str
    description: Optional[str]
    keywords: List[str]
    filters: Optional[Dict[str, Any]]
    frequency: AlertFrequency
    channels: List[NotificationChannel]
    is_active: bool
    last_triggered_at: Optional[datetime]
    last_sent_at: Optional[datetime]
    trigger_count: int
    match_count: int
    created_at: datetime
    updated_at: datetime
    
    # Computed
    filter_summary: Optional[str] = None
    matches_today: int = 0
    matches_this_week: int = 0


class AlertListResponse(BaseModel):
    """Schema for paginated alert list response."""
    
    alerts: List[AlertResponse]
    total: int
    active_count: int
    inactive_count: int


class AlertTrigger(BaseModel):
    """Schema for alert trigger payload."""
    
    alert_id: uuid.UUID
    tender_ids: List[uuid.UUID]
    match_count: int
    triggered_at: datetime


class AlertTestRequest(BaseModel):
    """Schema for testing an alert."""
    
    keywords: List[str]
    filters: Optional[AlertFilters] = None
    limit: int = Field(5, ge=1, le=50)


class AlertTestResponse(BaseModel):
    """Schema for alert test results."""
    
    matching_tenders: List[Dict[str, Any]]
    total_matches: int
    search_time_ms: int
    preview_message: str
