"""
Subscription model for Hotmart API
"""

from typing import Optional
from pydantic import BaseModel


class Subscription(BaseModel):
    """Subscription model based on Hotmart API response"""
    id: str
    product_id: str
    customer_id: str
    status: str
    plan_name: str
    price: float
    currency: str
    billing_cycle: str
    created_date: str
    next_charge_date: Optional[str] = None
    cancelled_date: Optional[str] = None


class SubscriptionListResponse(BaseModel):
    """Response model for subscription listing"""
    total_subscriptions: int
    returned_count: int
    offset: int
    limit: int
    subscriptions: list[Subscription]
    summary: str
