"""
Tender schemas for search and display.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum
import uuid
from decimal import Decimal


class ProcurementType(str, Enum):
    """Procurement type enumeration."""
    GOODS = "goods"
    SERVICES = "services"
    WORKS = "works"
    CONSULTANCY = "consultancy"


class TenderType(str, Enum):
    """Tender type enumeration."""
    OPEN = "open"
    LIMITED = "limited"
    SINGLE_SOURCE = "single_source"
    GE_M = "ge_m"


class TenderStatus(str, Enum):
    """Tender status enumeration."""
    ACTIVE = "active"
    CLOSED = "closed"
    CANCELLED = "cancelled"
    AWARDED = "awarded"
    EXPIRED = "expired"


class TenderFilters(BaseModel):
    """Schema for tender search filters."""
    
    # Text search
    query: Optional[str] = Field(None, max_length=500)
    
    # Location filters
    states: Optional[List[str]] = None
    districts: Optional[List[str]] = None
    cities: Optional[List[str]] = None
    
    # Category filters
    departments: Optional[List[str]] = None
    categories: Optional[List[str]] = None
    sub_categories: Optional[List[str]] = None
    
    # Type filters
    procurement_types: Optional[List[ProcurementType]] = None
    tender_types: Optional[List[TenderType]] = None
    
    # Status filters
    statuses: Optional[List[TenderStatus]] = None
    
    # Financial filters
    min_bid_value: Optional[float] = None
    max_bid_value: Optional[float] = None
    min_emd: Optional[float] = None
    max_emd: Optional[float] = None
    
    # Date filters
    publish_date_from: Optional[date] = None
    publish_date_to: Optional[date] = None
    closing_date_from: Optional[date] = None
    closing_date_to: Optional[date] = None
    closing_within_days: Optional[int] = Field(None, ge=1, le=365)
    
    # Source filters
    source_portals: Optional[List[str]] = None
    
    # Eligibility filters
    mse_exempted: Optional[bool] = None
    startup_exempted: Optional[bool] = None
    oem_required: Optional[bool] = None
    
    # Other filters
    has_corrigendum: Optional[bool] = None
    is_urgent: Optional[bool] = None
    min_experience_years: Optional[int] = None
    
    # Pagination
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
    
    # Sorting
    sort_by: str = Field("closing_date", pattern="^(title|publish_date|closing_date|bid_value_min|bid_value_max|created_at)$")
    sort_order: str = Field("asc", pattern="^(asc|desc)$")


class TenderSearchRequest(BaseModel):
    """Schema for tender search request."""
    
    filters: Optional[TenderFilters] = None
    keywords: Optional[List[str]] = None
    exclude_keywords: Optional[List[str]] = None
    saved_search_id: Optional[uuid.UUID] = None


class TenderResponse(BaseModel):
    """Schema for single tender response."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    tender_id: str
    tender_number: Optional[str]
    title: str
    description: Optional[str]
    
    # Buyer info
    department: Optional[str]
    buyer_name: Optional[str]
    authority: Optional[str]
    organization_type: Optional[str]
    
    # Location
    state: Optional[str]
    district: Optional[str]
    city: Optional[str]
    pincode: Optional[str]
    
    # Category
    category: Optional[str]
    sub_category: Optional[str]
    
    # Type
    procurement_type: Optional[ProcurementType]
    tender_type: Optional[TenderType]
    
    # Financial
    bid_value_min: Optional[Decimal]
    bid_value_max: Optional[Decimal]
    emd_amount: Optional[Decimal]
    currency: Optional[str]
    
    # Dates
    publish_date: Optional[date]
    opening_date: Optional[date]
    closing_date: Optional[date]
    corrigendum_date: Optional[date]
    
    # Status
    status: TenderStatus
    
    # Source
    source_url: Optional[str]
    source_portal: Optional[str]
    
    # Documents
    pdf_urls: Optional[List[str]]
    document_count: Optional[int]
    
    # Eligibility
    eligibility_criteria: Optional[Dict[str, Any]]
    turnover_required: Optional[Decimal]
    experience_years: Optional[int]
    mse_exemption: Optional[bool]
    startup_exemption: Optional[bool]
    
    # AI Analysis
    ai_summary: Optional[str]
    risk_score: Optional[int]
    complexity_score: Optional[int]
    qualification_probability: Optional[float]
    red_flags: Optional[List[str]]
    
    # Tracking
    view_count: int
    saved_count: int
    
    # Corrigendum
    is_corrigendum: bool
    corrigendum_count: int
    
    # Award info
    awarded_bidder: Optional[str]
    awarded_amount: Optional[Decimal]
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    
    # Computed fields
    days_to_close: Optional[int] = None
    is_urgent: bool = False
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "tender_id": "GEM-2024-123456",
                "title": "Annual Housekeeping Services for Government Office",
                "department": "Ministry of Home Affairs",
                "state": "Delhi",
                "closing_date": "2024-12-31",
                "bid_value_max": 5000000,
                "status": "active",
            }
        }


class TenderListResponse(BaseModel):
    """Schema for paginated tender list response."""
    
    tenders: List[TenderResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool
    
    # Search metadata
    search_time_ms: Optional[int] = None
    facets: Optional[Dict[str, Any]] = None


class TenderStats(BaseModel):
    """Schema for tender statistics."""
    
    total_active: int
    total_closed: int
    total_today: int
    total_this_week: int
    total_this_month: int
    urgent_count: int  # Closing within 7 days
    corrigendum_count: int
    
    # By category
    by_procurement_type: Dict[str, int]
    by_state: Dict[str, int]
    by_department: Dict[str, int]
    
    # Value ranges
    avg_bid_value: Optional[Decimal]
    median_bid_value: Optional[Decimal]
    
    # Trend data (last 30 days)
    daily_counts: List[Dict[str, Any]]
