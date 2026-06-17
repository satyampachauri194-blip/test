"""
Tender model for storing government procurement opportunities.
"""

from sqlalchemy import Column, String, Text, Integer, Float, Boolean, DateTime, Date, Enum as SQLEnum, DECIMAL, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP, JSONB
from sqlalchemy.sql import func
import uuid
import enum

from app.db.session import Base


class ProcurementType(enum.Enum):
    """Type of procurement."""
    GOODS = "goods"
    SERVICES = "services"
    WORKS = "works"
    CONSULTANCY = "consultancy"


class TenderType(enum.Enum):
    """Type of tender process."""
    OPEN = "open"
    LIMITED = "limited"
    SINGLE_SOURCE = "single_source"
    GE_M = "ge_m"


class TenderStatus(enum.Enum):
    """Status of a tender."""
    ACTIVE = "active"
    CLOSED = "closed"
    CANCELLED = "cancelled"
    AWARDED = "awarded"
    EXPIRED = "expired"


class Tender(Base):
    """
    Tender model representing government procurement opportunities.
    
    Stores comprehensive information about tenders including:
    - Basic details (title, description, dates)
    - Buyer information (department, authority, location)
    - Financial details (bid value, EMD)
    - Eligibility criteria
    - AI-generated analysis
    - Documents and PDFs
    """
    
    __tablename__ = "tenders"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Identification
    tender_id = Column(VARCHAR(100), unique=True, nullable=False, index=True)  # External tender ID
    tender_number = Column(VARCHAR(100), nullable=True, index=True)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    
    # Buyer information
    department = Column(VARCHAR(255), nullable=True, index=True)
    buyer_name = Column(VARCHAR(255), nullable=True)
    authority = Column(VARCHAR(255), nullable=True)
    organization_type = Column(VARCHAR(100), nullable=True)  # Central Govt, State Govt, PSU, etc.
    
    # Location
    state = Column(VARCHAR(100), nullable=True, index=True)
    district = Column(VARCHAR(100), nullable=True, index=True)
    city = Column(VARCHAR(100), nullable=True)
    pincode = Column(VARCHAR(10), nullable=True)
    address = Column(Text, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Category
    category = Column(VARCHAR(100), nullable=True, index=True)
    sub_category = Column(VARCHAR(100), nullable=True)
    cpv_code = Column(VARCHAR(20), nullable=True)  # Common Procurement Vocabulary
    
    # Procurement details
    procurement_type = Column(SQLEnum(ProcurementType), nullable=True)
    tender_type = Column(SQLEnum(TenderType), nullable=True)
    
    # Financial details
    bid_value_min = Column(DECIMAL(15, 2), nullable=True)
    bid_value_max = Column(DECIMAL(15, 2), nullable=True)
    emd_amount = Column(DECIMAL(15, 2), nullable=True)
    currency = Column(VARCHAR(3), default="INR", nullable=True)
    
    # Important dates
    publish_date = Column(Date, nullable=True, index=True)
    opening_date = Column(Date, nullable=True)
    closing_date = Column(Date, nullable=True, index=True)
    corrigendum_date = Column(Date, nullable=True)
    pre_bid_date = Column(Date, nullable=True)
    award_date = Column(Date, nullable=True)
    
    # Status
    status = Column(SQLEnum(TenderStatus), default=TenderStatus.ACTIVE, nullable=False, index=True)
    
    # Source information
    source_url = Column(Text, nullable=True)
    source_portal = Column(VARCHAR(100), nullable=True, index=True)  # GeM, CPPP, etc.
    portal_tender_id = Column(VARCHAR(100), nullable=True)
    
    # Documents
    pdf_urls = Column(JSONB, default=list, nullable=True)
    document_count = Column(Integer, default=0, nullable=True)
    
    # Eligibility criteria (structured)
    eligibility_criteria = Column(JSONB, default=dict, nullable=True)
    turnover_required = Column(DECIMAL(15, 2), nullable=True)
    experience_years = Column(Integer, nullable=True)
    similar_work_required = Column(Boolean, default=False, nullable=True)
    oem_authorization = Column(Boolean, default=False, nullable=True)
    mse_exemption = Column(Boolean, default=True, nullable=True)
    startup_exemption = Column(Boolean, default=True, nullable=True)
    
    # Technical specifications
    technical_specifications = Column(JSONB, default=dict, nullable=True)
    
    # Financial criteria
    financial_criteria = Column(JSONB, default=dict, nullable=True)
    
    # Documents required
    documents_required = Column(JSONB, default=list, nullable=True)
    
    # AI Analysis
    ai_summary = Column(Text, nullable=True)
    risk_score = Column(Integer, nullable=True)  # 0-100
    complexity_score = Column(Integer, nullable=True)  # 0-100
    qualification_probability = Column(Float, nullable=True)  # 0-1
    red_flags = Column(JSONB, default=list, nullable=True)
    compliance_checklist = Column(JSONB, default=dict, nullable=True)
    extracted_atc = Column(JSONB, default=list, nullable=True)  # Additional Terms and Conditions
    extracted_boq = Column(JSONB, default=list, nullable=True)  # Bill of Quantities
    
    # Tracking
    view_count = Column(Integer, default=0, nullable=True)
    download_count = Column(Integer, default=0, nullable=True)
    saved_count = Column(Integer, default=0, nullable=True)
    
    # Corrigendum tracking
    is_corrigendum = Column(Boolean, default=False, nullable=True)
    original_tender_id = Column(UUID(as_uuid=True), ForeignKey("tenders.id"), nullable=True)
    corrigendum_count = Column(Integer, default=0, nullable=True)
    
    # Award information
    awarded_bidder = Column(VARCHAR(255), nullable=True)
    awarded_amount = Column(DECIMAL(15, 2), nullable=True)
    l1_bidder = Column(VARCHAR(255), nullable=True)
    l1_amount = Column(DECIMAL(15, 2), nullable=True)
    
    # Timestamps
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    scraped_at = Column(TIMESTAMP(timezone=True), nullable=True)
    last_synced_at = Column(TIMESTAMP(timezone=True), nullable=True)
    
    # Indexes
    __table_args__ = (
        Index('idx_tenders_location', 'state', 'district'),
        Index('idx_tenders_dates', 'publish_date', 'closing_date'),
        Index('idx_tenders_value', 'bid_value_min', 'bid_value_max'),
        Index('idx_tenders_full_text', 'title', 'description', postgresql_using='gin',
              postgresql_ops={'title': 'gin_trgm_ops', 'description': 'gin_trgm_ops'}),
    )
    
    def __repr__(self) -> str:
        return f"<Tender {self.tender_id}: {self.title[:50]}>"
    
    @property
    def is_active(self) -> bool:
        """Check if tender is currently active."""
        return self.status == TenderStatus.ACTIVE
    
    @property
    def days_to_close(self) -> int | None:
        """Get number of days until tender closes."""
        from datetime import date
        if self.closing_date:
            delta = self.closing_date - date.today()
            return delta.days
        return None
    
    @property
    def is_urgent(self) -> bool:
        """Check if tender is closing within 7 days."""
        days = self.days_to_close
        return days is not None and 0 <= days <= 7
    
    @property
    def has_corrigendum(self) -> bool:
        """Check if tender has any corrigendum."""
        return self.is_corrigendum or self.corrigendum_count > 0
