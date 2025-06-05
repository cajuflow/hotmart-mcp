"""
Product model for Hotmart API
"""

from typing import Optional
from pydantic import BaseModel


class Product(BaseModel):
    """Product model based on Hotmart API response"""
    id: int
    name: str
    ucode: str
    status: str
    created_at: int  # timestamp
    format: str
    is_subscription: bool
    warranty_period: int


class PageInfo(BaseModel):
    """Page info for pagination"""
    next_page_token: Optional[str] = None
    prev_page_token: Optional[str] = None
    results_per_page: int


class ProductListResponse(BaseModel):
    """Response model for product listing"""
    items: list[Product]
    page_info: PageInfo
