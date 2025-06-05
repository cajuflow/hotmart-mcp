"""
Product management tool for Hotmart MCP
"""

import json
import logging
from typing import Optional

from .base import api_client, format_error, validate_max_results, validate_status, validate_format

logger = logging.getLogger("hotmart-tools.products")


async def get_products(
    status: Optional[str] = None,
    max_results: int = 50,
    page_token: Optional[str] = None,
    product_id: Optional[str] = None,
    format: Optional[str] = None
) -> str:
    """
    Get list of products from Hotmart account.
    
    Args:
        status: Filter by product status. Options: DRAFT, ACTIVE, PAUSED, NOT_APPROVED, IN_REVIEW, DELETED, CHANGES_PENDING_ON_PRODUCT
        max_results: Maximum number of items per page (default: 50, max: 50)
        page_token: Cursor for pagination
        product_id: Unique identifier (ID) of the product (7 digits)
        format: Product format. Options: EBOOK, SOFTWARE, MOBILE_APPS, VIDEOS, AUDIOS, TEMPLATES, IMAGES, ONLINE_COURSE, SERIAL_CODES, ETICKET, ONLINE_SERVICE, ONLINE_EVENT, BUNDLE, COMMUNITY
    
    Returns:
        JSON string containing list of products with their details
    """
    try:
        logger.info(f"Fetching products with status={status}, max_results={max_results}, page_token={page_token}, product_id={product_id}, format={format}")
        
        # Validate status parameter
        if status:
            status_error = validate_status(status)
            if status_error:
                return format_error(status_error)
        
        # Validate max_results parameter
        max_results_error = validate_max_results(max_results)
        if max_results_error:
            return format_error(max_results_error)
        
        # Validate format parameter
        if format:
            format_error_msg = validate_format(format)
            if format_error_msg:
                return format_error(format_error_msg)
        
        # Fetch products from Hotmart API
        response = await api_client.get_products(
            status=status,
            max_results=max_results,
            page_token=page_token,
            product_id=product_id,
            format=format
        )
        
        # Extract products from response
        items = response.get("items", [])
        page_info = response.get("page_info", {})
        
        # Format response
        result = {
            "total_items": len(items),
            "page_info": page_info,
            "items": []
        }
        
        # Process each product
        for product_data in items:
            try:
                # Convert timestamp to readable date
                from datetime import datetime
                created_date = datetime.fromtimestamp(product_data.get("created_at", 0) / 1000).isoformat()
                
                product = {
                    "id": product_data.get("id"),
                    "name": product_data.get("name", ""),
                    "ucode": product_data.get("ucode", ""),
                    "status": product_data.get("status", ""),
                    "created_at": product_data.get("created_at"),
                    "created_date": created_date,
                    "format": product_data.get("format", ""),
                    "is_subscription": product_data.get("is_subscription", False),
                    "warranty_period": product_data.get("warranty_period", 0)
                }
                result["items"].append(product)
            except Exception as e:
                logger.warning(f"Error processing product data: {e}")
                continue
        
        # Add summary message
        filters = []
        if status:
            filters.append(f"status='{status}'")
        if format:
            filters.append(f"format='{format}'")
        if product_id:
            filters.append(f"id='{product_id}'")
        
        filter_text = f" with {', '.join(filters)}" if filters else ""
        summary = f"Found {len(items)} products{filter_text}"
        
        if page_info.get("next_page_token"):
            summary += f". Use page_token='{page_info['next_page_token']}' to get next page."
        if page_info.get("prev_page_token"):
            summary += f" Use page_token='{page_info['prev_page_token']}' for previous page."
        
        result["summary"] = summary
        
        return json.dumps(result, indent=2, ensure_ascii=False)
        
    except Exception as e:
        error_msg = f"Error fetching products: {str(e)}"
        logger.error(error_msg)
        return format_error(error_msg)
