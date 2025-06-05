"""
Test imports functionality
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_imports():
    """Test if all imports work correctly"""
    print("🔍 Testing imports...")
    
    try:
        # Test basic imports
        from hotmart.config import HOTMART_ENVIRONMENT, BASE_URL, ENDPOINTS
        print(f"✅ Config imported - Environment: {HOTMART_ENVIRONMENT}")
        
        # Test auth imports
        from hotmart.auth import AuthService
        print("✅ Auth service imported")
        
        # Test model imports (individual imports to pinpoint issues)
        from hotmart.models.base import ApiResponse, AuthToken
        print("✅ Base models imported")
        
        from hotmart.models.product import Product, ProductListResponse
        print("✅ Product models imported")
        
        from hotmart.models.sale import Sale, SalesListResponse, SalesPageInfo
        print("✅ Sale models imported")
        
        from hotmart.models.subscription import Subscription, SubscriptionListResponse
        print("✅ Subscription models imported")
        
        # Test client import
        from hotmart.client import HotmartApiClient
        print("✅ Client imported")
        
        # Test tools imports
        from hotmart.tools.base import api_client, cleanup_api_client, format_error
        from hotmart.tools.products import get_products
        from hotmart.tools.sales import get_sales_history
        print("✅ Tools imported")
        
        # Test package level imports
        from hotmart.tools import get_products as package_products
        from hotmart.tools import get_sales_history as package_sales
        from hotmart.tools import cleanup
        print("✅ Package level imports working")
        
        # Test server imports
        from hotmart_mcp import mcp
        print("✅ MCP server imports working")
        
        print("🎉 All imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_imports()
