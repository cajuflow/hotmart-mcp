"""
Authentication service for Hotmart API
"""

import logging
from datetime import datetime, timedelta
from typing import Optional

import httpx

from .config import (
    HOTMART_CLIENT_ID,
    HOTMART_CLIENT_SECRET, 
    HOTMART_BASIC_TOKEN,
    HOTMART_TIMEOUT,
    AUTH_URL,
    ENDPOINTS
)
from .models import AuthToken

logger = logging.getLogger("hotmart-auth")


class AuthService:
    """Handles OAuth 2.0 authentication with Hotmart API"""
    
    def __init__(self):
        self.access_token: Optional[str] = None
        self.token_expires_at: Optional[datetime] = None
        self.client = httpx.AsyncClient(timeout=HOTMART_TIMEOUT)
    
    async def get_access_token(self) -> str:
        """Get a valid access token, refreshing if necessary"""
        if self.access_token and self.token_expires_at and datetime.now() < self.token_expires_at:
            return self.access_token
        
        await self._refresh_token()
        return self.access_token
    
    async def _refresh_token(self) -> None:
        """Refresh the access token using client credentials flow"""
        try:
            logger.info(f"Requesting token from: {AUTH_URL}{ENDPOINTS['AUTH_TOKEN']}")
            
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json"
            }
            
            # Add Basic token if provided (some Hotmart integrations require it)
            if HOTMART_BASIC_TOKEN:
                headers["Authorization"] = f"Basic {HOTMART_BASIC_TOKEN}"
                logger.info("Using Basic token for authentication")
            
            # Hotmart expects form data with client credentials
            data = {
                "grant_type": "client_credentials",
                "client_id": HOTMART_CLIENT_ID,
                "client_secret": HOTMART_CLIENT_SECRET
            }
            
            logger.debug(f"Request headers: {headers}")
            logger.debug(f"Request data: {data}")
            
            response = await self.client.post(
                f"{AUTH_URL}{ENDPOINTS['AUTH_TOKEN']}",
                headers=headers,
                data=data  # Use data instead of json for form encoding
            )
            
            response.raise_for_status()
            token_data = response.json()
            
            self.access_token = token_data["access_token"]
            expires_in = token_data.get("expires_in", 3600)
            
            # Set expiration with 60 second buffer
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in - 60)
            
            logger.info("Successfully refreshed Hotmart access token")
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error during token refresh: {e.response.status_code}")
            logger.error(f"Response body: {e.response.text}")
            logger.error(f"Request URL: {e.request.url}")
            logger.error(f"Request headers: {dict(e.request.headers)}")
            raise
        except Exception as e:
            logger.error(f"Failed to refresh Hotmart token: {e}")
            raise
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
    
    def clear_token(self):
        """Clear the current token (force refresh on next request)"""
        self.access_token = None
        self.token_expires_at = None
    
    def is_token_valid(self) -> bool:
        """Check if current token is valid and not expired"""
        if not self.access_token or not self.token_expires_at:
            return False
        return datetime.now() < self.token_expires_at
