"""
Subscription model for SaaS monetization.
"""

from sqlalchemy import Column, String, Boolean, DateTime, Date, Enum as SQLEnum, DECIMAL, ForeignKey, VARCHAR
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy.sql import func
import uuid
import enum

from app.db.session import Base


class PlanType(enum.Enum):
    """Subscription plan types."""
    FREE = "free"
    STARTER = "starter"
    PROFESSIONAL = "professional"
    BUSINESS = "business"
    ENTERPRISE = "enterprise"


class SubscriptionStatus(enum.Enum):
    """Subscription status."""
    ACTIVE = "active"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    PAST_DUE = "past_due"
    TRIAL = "trial"


class Subscription(Base):
    """
    Subscription model for managing user subscriptions and billing.
    
    Tracks subscription lifecycle, payments, and renewal information.
    """
    
    __tablename__ = "subscriptions"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign key to user
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # Plan details
    plan_type = Column(SQLEnum(PlanType), default=PlanType.FREE, nullable=False, index=True)
    status = Column(SQLEnum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE, nullable=False, index=True)
    
    # Billing period
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False, index=True)
    trial_start_date = Column(Date, nullable=True)
    trial_end_date = Column(Date, nullable=True)
    
    # Payment details
    amount = Column(DECIMAL(10, 2), nullable=True)
    currency = Column(VARCHAR(3), default="INR", nullable=True)
    billing_cycle = Column(VARCHAR(20), default="monthly", nullable=True)  # monthly, yearly
    
    # Payment gateway
    payment_gateway = Column(VARCHAR(50), nullable=True)  # razorpay, stripe
    payment_id = Column(VARCHAR(100), nullable=True)
    order_id = Column(VARCHAR(100), nullable=True)
    signature = Column(String, nullable=True)
    
    # Auto-renewal
    auto_renew = Column(Boolean, default=True, nullable=True)
    cancellation_reason = Column(String, nullable=True)
    cancelled_at = Column(TIMESTAMP(timezone=True), nullable=True)
    
    # Usage tracking (for current period)
    searches_used = Column(Integer, default=0, nullable=True)
    pdf_downloads_used = Column(Integer, default=0, nullable=True)
    ai_analyses_used = Column(Integer, default=0, nullable=True)
    last_usage_reset = Column(Date, default=func.now(), nullable=True)
    
    # Invoice
    invoice_url = Column(String, nullable=True)
    invoice_number = Column(VARCHAR(50), nullable=True)
    gst_amount = Column(DECIMAL(10, 2), nullable=True)
    total_amount = Column(DECIMAL(10, 2), nullable=True)
    
    # Coupons
    coupon_code = Column(VARCHAR(50), nullable=True)
    discount_amount = Column(DECIMAL(10, 2), nullable=True)
    
    # Timestamps
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self) -> str:
        return f"<Subscription {self.user_id}: {self.plan_type.value}>"
    
    @property
    def is_active(self) -> bool:
        """Check if subscription is currently active."""
        return self.status == SubscriptionStatus.ACTIVE
    
    @property
    def is_trial(self) -> bool:
        """Check if subscription is in trial period."""
        return self.status == SubscriptionStatus.TRIAL
    
    @property
    def days_remaining(self) -> int | None:
        """Get number of days until subscription expires."""
        from datetime import date
        if self.end_date:
            delta = self.end_date - date.today()
            return max(0, delta.days)
        return None
    
    @property
    def will_auto_renew(self) -> bool:
        """Check if subscription will auto-renew."""
        return self.auto_renew and self.is_active
    
    def get_plan_pricing(self) -> dict:
        """Get pricing information for the plan."""
        pricing = {
            PlanType.FREE: {
                "monthly": 0,
                "yearly": 0,
                "features": [
                    "10 daily searches",
                    "No PDF downloads",
                    "No AI analysis",
                    "5 saved tenders",
                    "1 alert",
                    "7 days historical data",
                ],
            },
            PlanType.STARTER: {
                "monthly": 999,
                "yearly": 9999,
                "features": [
                    "50 daily searches",
                    "5 PDF downloads/month",
                    "3 AI analyses/month",
                    "25 saved tenders",
                    "3 alerts",
                    "30 days historical data",
                    "CSV export",
                ],
            },
            PlanType.PROFESSIONAL: {
                "monthly": 2499,
                "yearly": 24999,
                "features": [
                    "200 daily searches",
                    "25 PDF downloads/month",
                    "15 AI analyses/month",
                    "100 saved tenders",
                    "10 alerts",
                    "90 days historical data",
                    "CSV + Excel export",
                    "API access",
                    "Team collaboration (5 members)",
                ],
            },
            PlanType.BUSINESS: {
                "monthly": 4999,
                "yearly": 49999,
                "features": [
                    "1000 daily searches",
                    "100 PDF downloads/month",
                    "50 AI analyses/month",
                    "500 saved tenders",
                    "25 alerts",
                    "1 year historical data",
                    "All export formats",
                    "Full API access",
                    "Team collaboration (20 members)",
                    "Priority support",
                    "Custom integrations",
                ],
            },
            PlanType.ENTERPRISE: {
                "monthly": 9999,
                "yearly": 99999,
                "features": [
                    "Unlimited searches",
                    "Unlimited PDF downloads",
                    "Unlimited AI analyses",
                    "Unlimited saved tenders",
                    "Unlimited alerts",
                    "5 years historical data",
                    "Full API access with webhooks",
                    "Team collaboration (100 members)",
                    "Dedicated account manager",
                    "Custom training",
                    "SLA guarantee",
                    "White-label options",
                ],
            },
        }
        return pricing.get(self.plan_type, pricing[PlanType.FREE])
