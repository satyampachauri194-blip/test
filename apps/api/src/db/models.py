"""
Database Models
Core entities for Tender Intelligence AI platform
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text, JSON, ForeignKey, Index, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
import enum

from src.db.session import Base


class UserRole(enum.Enum):
    FREE = "free"
    STARTER = "starter"
    PROFESSIONAL = "professional"
    BUSINESS = "business"
    ENTERPRISE = "enterprise"
    ADMIN = "admin"


class TenderStatus(enum.Enum):
    ACTIVE = "active"
    CLOSED = "closed"
    CANCELLED = "cancelled"
    AWARDED = "awarded"
    AMENDED = "amended"


class User(Base):
    """User model for authentication and profile"""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    phone = Column(String(20))
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"))
    role = Column(SQLEnum(UserRole), default=UserRole.FREE)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    last_login = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    organization = relationship("Organization", back_populates="users")
    saved_tenders = relationship("SavedTender", back_populates="user")
    searches = relationship("SavedSearch", back_populates="user")
    subscriptions = relationship("Subscription", back_populates="user")


class Organization(Base):
    """Organization model for multi-tenant support"""
    __tablename__ = "organizations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    gst_number = Column(String(15))
    pan_number = Column(String(10))
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(100))
    pincode = Column(String(6))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    users = relationship("User", back_populates="organization")
    subscriptions = relationship("Subscription", back_populates="organization")


class Tender(Base):
    """Core tender model with normalized structure"""
    __tablename__ = "tenders"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tender_id = Column(String(100), unique=True, nullable=False, index=True)
    tender_number = Column(String(100), index=True)
    title = Column(Text, nullable=False)
    description = Column(Text)
    status = Column(SQLEnum(TenderStatus), default=TenderStatus.ACTIVE)
    
    # Buyer info
    buyer_name = Column(String(255), index=True)
    buyer_department = Column(String(255), index=True)
    buyer_organization = Column(String(255))
    
    # Location
    state = Column(String(100), index=True)
    district = Column(String(100), index=True)
    city = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    
    # Dates
    publish_date = Column(DateTime, index=True)
    closing_date = Column(DateTime, index=True)
    opening_date = Column(DateTime)
    modified_date = Column(DateTime)
    
    # Financial
    tender_value_min = Column(Float)
    tender_value_max = Column(Float)
    emd_amount = Column(Float)
    currency = Column(String(3), default="INR")
    
    # Classification
    category = Column(String(100), index=True)  # Goods/Services/Works
    sub_category = Column(String(100))
    nic_code = Column(String(10))
    
    # Source
    source_url = Column(Text)
    source_portal = Column(String(100), index=True)  # GeM, CPPP, etc.
    
    # Documents
    document_count = Column(Integer, default=0)
    has_corrigendum = Column(Boolean, default=False)
    
    # Eligibility
    is_mse_exempt = Column(Boolean, default=False)
    is_startup_exempt = Column(Boolean, default=False)
    turnover_required = Column(Float)
    experience_required = Column(Integer)  # years
    
    # Metadata
    raw_data = Column(JSONB)
    search_vector = Column(Text)  # For full-text search
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Indexes
    __table_args__ = (
        Index('idx_tender_dates', 'publish_date', 'closing_date'),
        Index('idx_tender_location', 'state', 'district'),
        Index('idx_tender_value', 'tender_value_min', 'tender_value_max'),
    )
    
    # Relationships
    documents = relationship("TenderDocument", back_populates="tender")
    ai_analysis = relationship("TenderAIAnalysis", back_populates="tender", uselist=False)
    saved_by = relationship("SavedTender", back_populates="tender")


class TenderDocument(Base):
    """Tender documents and PDFs"""
    __tablename__ = "tender_documents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tender_id = Column(UUID(as_uuid=True), ForeignKey("tenders.id"), nullable=False)
    document_type = Column(String(50))  # RFP, BOQ, Corrigendum, etc.
    file_name = Column(String(255))
    file_url = Column(Text, nullable=False)
    file_size = Column(Integer)  # bytes
    storage_path = Column(String(500))
    is_parsed = Column(Boolean, default=False)
    parsed_content = Column(JSONB)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    tender = relationship("Tender", back_populates="documents")


class TenderAIAnalysis(Base):
    """AI-powered analysis of tenders"""
    __tablename__ = "tender_ai_analyses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tender_id = Column(UUID(as_uuid=True), ForeignKey("tenders.id"), unique=True)
    
    # Extracted data
    eligibility_criteria = Column(JSONB)
    technical_requirements = Column(JSONB)
    financial_requirements = Column(JSONB)
    key_dates = Column(JSONB)
    risk_factors = Column(JSONB)
    
    # Scores
    risk_score = Column(Integer)  # 0-100
    complexity_score = Column(Integer)  # 0-100
    qualification_probability = Column(Float)  # 0-1
    
    # Generated content
    summary = Column(Text)
    red_flags = Column(JSONB)
    compliance_checklist = Column(JSONB)
    required_documents = Column(JSONB)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tender = relationship("Tender", back_populates="ai_analysis")


class SavedTender(Base):
    """User saved tenders"""
    __tablename__ = "saved_tenders"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    tender_id = Column(UUID(as_uuid=True), ForeignKey("tenders.id"), nullable=False)
    notes = Column(Text)
    tags = Column(JSONB, default=list)
    is_following = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="saved_tenders")
    tender = relationship("Tender", back_populates="saved_by")
    
    __table_args__ = (
        Index('idx_saved_tender_user', 'user_id', 'tender_id', unique=True),
    )


class SavedSearch(Base):
    """User saved searches for alerts"""
    __tablename__ = "saved_searches"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    keywords = Column(JSONB)  # Search criteria
    filters = Column(JSONB)  # Additional filters
    frequency = Column(String(20), default="daily")  # instant, daily, weekly
    is_active = Column(Boolean, default=True)
    last_sent = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="searches")


class Subscription(Base):
    """User subscriptions and billing"""
    __tablename__ = "subscriptions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"))
    plan_type = Column(String(50), nullable=False)  # free, starter, professional, etc.
    status = Column(String(20), default="active")
    
    # Billing
    amount = Column(Float)
    currency = Column(String(3), default="INR")
    payment_provider = Column(String(20))  # razorpay, stripe
    payment_id = Column(String(100))
    
    # Period
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    auto_renew = Column(Boolean, default=True)
    
    # Usage tracking
    searches_used = Column(Integer, default=0)
    downloads_used = Column(Integer, default=0)
    ai_analyses_used = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="subscriptions")
    organization = relationship("Organization", back_populates="subscriptions")


class AuditLog(Base):
    """Audit trail for security and compliance"""
    __tablename__ = "audit_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50))
    resource_id = Column(String(100))
    ip_address = Column(String(45))
    user_agent = Column(Text)
    metadata = Column(JSONB)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
