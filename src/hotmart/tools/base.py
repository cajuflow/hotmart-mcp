"""
Base classes and utilities for tools
"""

import logging
from typing import Any
from ..client import HotmartApiClient

# Logger for tools
logger = logging.getLogger("hotmart-tools")

# Global API client instance
api_client = HotmartApiClient()


async def cleanup_api_client():
    """Cleanup function to close API client"""
    try:
        await api_client.close()
    except Exception as e:
        logger.error(f"Error during API client cleanup: {e}")


def format_error(error_message: str) -> str:
    """Format error message consistently"""
    return f"Error: {error_message}"


def validate_max_results(max_results: int) -> str | None:
    """Validate max_results parameter"""
    if max_results < 1 or max_results > 50:
        return "max_results must be between 1 and 50"
    return None


def validate_status(status: str) -> str | None:
    """Validate status parameter for products"""
    valid_statuses = ["DRAFT", "ACTIVE", "PAUSED", "NOT_APPROVED", "IN_REVIEW", "DELETED", "CHANGES_PENDING_ON_PRODUCT"]
    if status.upper() not in valid_statuses:
        return f"Invalid status '{status}'. Valid options are: {', '.join(valid_statuses)}"
    return None


def validate_format(format: str) -> str | None:
    """Validate format parameter for products"""
    valid_formats = ["EBOOK", "SOFTWARE", "MOBILE_APPS", "VIDEOS", "AUDIOS", "TEMPLATES", "IMAGES", "ONLINE_COURSE", "SERIAL_CODES", "ETICKET", "ONLINE_SERVICE", "ONLINE_EVENT", "BUNDLE", "COMMUNITY"]
    if format.upper() not in valid_formats:
        return f"Invalid format '{format}'. Valid options are: {', '.join(valid_formats)}"
    return None
