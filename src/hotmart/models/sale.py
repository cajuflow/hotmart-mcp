"""
Sale model for Hotmart API
"""

from typing import Optional
from pydantic import BaseModel


class Product(BaseModel):
    """Product information in sale"""
    name: str
    id: int


class Buyer(BaseModel):
    """Buyer information"""
    name: str
    ucode: str
    email: str


class Producer(BaseModel):
    """Producer information"""
    name: str
    ucode: str


class Price(BaseModel):
    """Price information"""
    value: float
    currency_code: str


class Payment(BaseModel):
    """Payment information"""
    method: str
    installments_number: int
    type: str


class Tracking(BaseModel):
    """Tracking information"""
    source_sck: str
    source: str
    external_code: str


class Offer(BaseModel):
    """Offer information"""
    payment_mode: str
    code: str


class HotmartFee(BaseModel):
    """Hotmart fee information"""
    total: float
    fixed: float
    currency_code: str
    base: float
    percentage: float


class Purchase(BaseModel):
    """Purchase information"""
    transaction: str
    order_date: int  # timestamp
    approved_date: int  # timestamp
    status: str
    recurrency_number: int
    is_subscription: bool
    commission_as: str
    price: Price
    payment: Payment
    tracking: Tracking
    warranty_expire_date: int  # timestamp
    offer: Offer
    hotmart_fee: HotmartFee


class Sale(BaseModel):
    """Sale model based on Hotmart API response"""
    product: Product
    buyer: Buyer
    producer: Producer
    purchase: Purchase


class SalesPageInfo(BaseModel):
    """Page info for sales pagination"""
    total_results: int
    next_page_token: Optional[str] = None
    prev_page_token: Optional[str] = None
    results_per_page: int


class SalesListResponse(BaseModel):
    """Response model for sales listing"""
    items: list[Sale]
    page_info: SalesPageInfo
