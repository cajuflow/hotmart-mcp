"""
Hotmart API client
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

import httpx

from .auth import AuthService
from .config import BASE_URL, ENDPOINTS, HOTMART_TIMEOUT, HOTMART_MAX_RETRIES
from .models import Product, Sale, Subscription

logger = logging.getLogger("hotmart-api")


class HotmartApiClient:
    """Main API client for Hotmart"""
    
    def __init__(self):
        self.auth = AuthService()
        self.client = httpx.AsyncClient(timeout=HOTMART_TIMEOUT)
    
    async def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make an authenticated request to the Hotmart API"""
        token = await self.auth.get_access_token()
        
        headers = kwargs.get("headers", {})
        headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
        kwargs["headers"] = headers
        
        url = f"{BASE_URL}{endpoint}"
        
        for attempt in range(HOTMART_MAX_RETRIES):
            try:
                logger.debug(f"Making {method} request to {url}")
                response = await self.client.request(method, url, **kwargs)
                response.raise_for_status()
                return response.json()
            
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 401 and attempt == 0:
                    # Token might be expired, refresh and retry
                    logger.info("Token expired, refreshing...")
                    await self.auth._refresh_token()
                    token = await self.auth.get_access_token()
                    headers["Authorization"] = f"Bearer {token}"
                    continue
                
                logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
                raise
            
            except Exception as e:
                if attempt == HOTMART_MAX_RETRIES - 1:
                    logger.error(f"API request failed after {HOTMART_MAX_RETRIES} attempts: {e}")
                    raise
                
                logger.warning(f"Request attempt {attempt + 1} failed: {e}, retrying...")
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
    
    async def get_products(self, status: Optional[str] = None, max_results: int = 50, 
                          page_token: Optional[str] = None, product_id: Optional[str] = None,
                          format: Optional[str] = None) -> Dict[str, Any]:
        """
        Get list of products from Hotmart
        
        Args:
            status: Filter by product status (DRAFT, ACTIVE, PAUSED, NOT_APPROVED, IN_REVIEW, DELETED, CHANGES_PENDING_ON_PRODUCT)
            max_results: Maximum number of items per page (default: 50, max: 50)
            page_token: Cursor for pagination
            product_id: Unique identifier (ID) of the product (7 digits)
            format: Product format (EBOOK, SOFTWARE, MOBILE_APPS, VIDEOS, AUDIOS, TEMPLATES, IMAGES, ONLINE_COURSE, SERIAL_CODES, ETICKET, ONLINE_SERVICE, ONLINE_EVENT, BUNDLE, COMMUNITY)
        """
        params = {
            "max_results": min(max_results, 50)
        }
        
        if status:
            params["status"] = status.upper()
        if page_token:
            params["page_token"] = page_token
        if product_id:
            params["id"] = product_id
        if format:
            params["format"] = format.upper()
        
        return await self._make_request("GET", ENDPOINTS["PRODUCTS"], params=params)
    
    async def get_sales_history(self, transaction_status: Optional[str] = None, max_results: int = 50,
                               page_token: Optional[str] = None, product_id: Optional[str] = None,
                               start_date: Optional[str] = None, end_date: Optional[str] = None,
                               sales_source: Optional[str] = None, transaction: Optional[str] = None,
                               buyer_name: Optional[str] = None, buyer_email: Optional[str] = None,
                               payment_type: Optional[str] = None, offer_code: Optional[str] = None,
                               commission_as: Optional[str] = None) -> Dict[str, Any]:
        """
        Get sales history from Hotmart
        
        Args:
            transaction_status: Status da transação (APPROVED, BLOCKED, CANCELLED, CHARGEBACK, COMPLETE, etc.)
            max_results: Número máximo de itens por página
            page_token: Cursor para paginação
            product_id: ID do produto (7 dígitos)
            start_date: Data inicial em milissegundos (timestamp)
            end_date: Data final em milissegundos (timestamp)
            sales_source: Código SRC da origem da venda
            transaction: Código único da transação
            buyer_name: Nome do comprador
            buyer_email: Email do comprador
            payment_type: Tipo de pagamento (BILLET, CREDIT_CARD, PIX, etc.)
            offer_code: Código da oferta
            commission_as: Como foi comissionado (PRODUCER, COPRODUCER, AFFILIATE)
        """
        params = {
            "max_results": min(max_results, 50)
        }
        
        if transaction_status:
            params["transaction_status"] = transaction_status.upper()
        if page_token:
            params["page_token"] = page_token
        if product_id:
            params["product_id"] = product_id
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        if sales_source:
            params["sales_source"] = sales_source
        if transaction:
            params["transaction"] = transaction
        if buyer_name:
            params["buyer_name"] = buyer_name
        if buyer_email:
            params["buyer_email"] = buyer_email
        if payment_type:
            params["payment_type"] = payment_type.upper()
        if offer_code:
            params["offer_code"] = offer_code
        if commission_as:
            params["commission_as"] = commission_as.upper()
        
        return await self._make_request("GET", ENDPOINTS["SALES_HISTORY"], params=params)
    
    async def get_subscriptions(self, status: Optional[str] = None, 
                               limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """
        Get subscriptions from Hotmart
        
        Args:
            status: Filter by subscription status (ACTIVE, CANCELLED, etc.)
            limit: Number of subscriptions to return
            offset: Pagination offset
        """
        params = {
            "limit": min(limit, 100),
            "offset": offset
        }
        
        if status:
            params["status"] = status.upper()
        
        return await self._make_request("GET", ENDPOINTS["SUBSCRIPTIONS"], params=params)
    
    async def close(self):
        """Close HTTP clients"""
        await self.auth.close()
        await self.client.aclose()
    
    async def test_connection(self) -> bool:
        """Test the API connection"""
        try:
            await self.auth.get_access_token()
            logger.info("✅ Successfully connected to Hotmart API")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to connect to Hotmart API: {e}")
            return False
