"""
Configuration and constants for Hotmart MCP
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Required Configuration
HOTMART_CLIENT_ID = os.getenv("HOTMART_CLIENT_ID")
HOTMART_CLIENT_SECRET = os.getenv("HOTMART_CLIENT_SECRET")
HOTMART_BASIC_TOKEN = os.getenv("HOTMART_BASIC_TOKEN")
HOTMART_ENVIRONMENT = os.getenv("HOTMART_ENVIRONMENT", "sandbox")

# Optional Configuration
HOTMART_TIMEOUT = int(os.getenv("HOTMART_TIMEOUT", "30"))
HOTMART_MAX_RETRIES = int(os.getenv("HOTMART_MAX_RETRIES", "3"))

# Validate required configuration
if not HOTMART_CLIENT_ID or not HOTMART_CLIENT_SECRET:
    raise ValueError("HOTMART_CLIENT_ID and HOTMART_CLIENT_SECRET are required")

# API URLs
BASE_URLS = {
    "sandbox": "https://sandbox.hotmart.com",
    "production": "https://developers.hotmart.com"
}

# Authentication URLs (different from main API)
AUTH_URLS = {
    "sandbox": "https://api-sec-vlc.hotmart.com",
    "production": "https://api-sec-vlc.hotmart.com"
}

BASE_URL = BASE_URLS.get(HOTMART_ENVIRONMENT, BASE_URLS["sandbox"])
AUTH_URL = AUTH_URLS.get(HOTMART_ENVIRONMENT, AUTH_URLS["sandbox"])

# API Endpoints
ENDPOINTS = {
    "AUTH_TOKEN": "/security/oauth/token",
    "PRODUCTS": "/products/api/v1/products",
    "SALES_HISTORY": "/payments/api/v1/sales/history",
    "SUBSCRIPTIONS": "/payments/api/v1/subscriptions"
}
