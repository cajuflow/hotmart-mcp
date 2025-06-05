"""
Base classes and common models
"""

from typing import Optional
from pydantic import BaseModel


class ApiResponse(BaseModel):
    """Generic API response wrapper"""
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None
    total: Optional[int] = None


class AuthToken(BaseModel):
    """Authentication token response"""
    access_token: str
    token_type: str
    expires_in: int
