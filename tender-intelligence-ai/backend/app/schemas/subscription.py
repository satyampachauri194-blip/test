"""
Subscription schemas for billing and plan management.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum
import uuid
from decimal import Decimal


class PlanType(str, Enum):
    """Subscription plan types."""
    FREE = "free"
    STARTER = "starter"
    PROFESSIONAL = "professional"
    BUSINESS = "business"
    ENTERPRISE = "enterprise"


class SubscriptionStatus(str, Enum):
    """Subscription status."""
    ACTIVE = "active"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    PAST_DUE = "past_due"
    TRIAL = "trial"


class BillingCycle(str, Enum):
    """Billing cycle options."""
    MONTHLY = "monthly"
    YEARLY = "yearly"


class PaymentGateway(str, Enum):
    """Payment gateway options."""
    RAZORPAY = "razorpay"
    STRIPE = "stripe"


class PlanFeatures(BaseModel):
    """Schema for plan features."""
    
    daily_searches: int
    pdf_downloads: int
    ai_analyses: int
    saved_tenders: int
    alerts: int
    team_members: int
    api_access: bool
    historical_data_days: int
    export_formats: List[str]


class PlanDetails(BaseModel):
    """Schema for subscription plan details."""
    
    plan_type: PlanType
    display_name: str
    description: str
    monthly_price: Decimal
    yearly_price: Decimal
    currency: str = "INR"
    features: List[str]
    limits: PlanFeatures
    popular: bool = False
    trial_days: int = 0


class SubscriptionResponse(BaseModel):
    """Schema for subscription response."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    user_id: uuid.UUID
    plan_type: PlanType
    status: SubscriptionStatus
    start_date: date
    end_date: date
    amount: Optional[Decimal]
    currency: Optional[str]
    billing_cycle: Optional[BillingCycle]
    payment_gateway: Optional[PaymentGateway]
    auto_renew: bool
    days_remaining: Optional[int]
    usage: Optional[Dict[str, int]]  # Current period usage
    created_at: datetime
    updated_at: datetime


class SubscriptionCreate(BaseModel):
    """Schema for creating a subscription."""
    
    plan_type: PlanType
    billing_cycle: BillingCycle = BillingCycle.MONTHLY
    coupon_code: Optional[str] = None
    trial: bool = False


class PaymentRequest(BaseModel):
    """Schema for payment initiation request."""
    
    plan_type: PlanType
    billing_cycle: BillingCycle
    amount: Decimal
    currency: str = "INR"
    gateway: PaymentGateway = PaymentGateway.RAZORPAY
    coupon_code: Optional[str] = None


class PaymentResponse(BaseModel):
    """Schema for payment response."""
    
    order_id: str
    amount: Decimal
    currency: str
    gateway: PaymentGateway
    checkout_url: Optional[str] = None
    razorpay_order: Optional[Dict[str, Any]] = None
    stripe_session: Optional[Dict[str, Any]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "order_id": "order_123456789",
                "amount": 2499.00,
                "currency": "INR",
                "gateway": "razorpay",
                "razorpay_order": {
                    "id": "order_123456789",
                    "amount": 249900,
                    "currency": "INR",
                }
            }
        }


class PaymentWebhook(BaseModel):
    """Schema for payment webhook payload."""
    
    entity: str
    event: str
    payment_id: Optional[str] = None
    order_id: Optional[str] = None
    subscription_id: Optional[str] = None
    amount: Optional[int] = None
    currency: Optional[str] = None
    status: Optional[str] = None
    signature: Optional[str] = None


class InvoiceResponse(BaseModel):
    """Schema for invoice response."""
    
    id: uuid.UUID
    invoice_number: str
    subscription_id: uuid.UUID
    amount: Decimal
    gst_amount: Decimal
    total_amount: Decimal
    currency: str
    status: str  # paid, pending, failed
    invoice_url: str
    created_at: datetime
    due_date: date


class CouponRequest(BaseModel):
    """Schema for coupon validation request."""
    
    code: str
    plan_type: PlanType


class CouponResponse(BaseModel):
    """Schema for coupon validation response."""
    
    valid: bool
    code: str
    discount_type: str  # percentage, fixed
    discount_value: Decimal
    max_discount: Optional[Decimal] = None
    min_purchase: Optional[Decimal] = None
    applicable_plans: Optional[List[PlanType]] = None
    expires_at: Optional[datetime] = None
    message: str
