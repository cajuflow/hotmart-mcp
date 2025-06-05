"""
Tests package for Hotmart MCP
"""

__version__ = "1.0.0"

# Test modules
from .test_imports import test_imports
from .test_config import test_config
from .test_auth import test_auth
from .test_client import test_client
from .test_products import test_products
from .test_sales import test_sales
from .test_tools import test_tools

__all__ = [
    "test_imports",
    "test_config", 
    "test_auth",
    "test_client",
    "test_products",
    "test_sales",
    "test_tools"
]
