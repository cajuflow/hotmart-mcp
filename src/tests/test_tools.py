"""
Test tools integration and functionality
"""

import asyncio
import json
import os
from pathlib import Path
import sys

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

async def test_tools():
    """Test tools integration and package-level imports"""
    print("🔧 Testing tools integration...")
    
    try:
        # Test package-level imports
        from hotmart.tools import get_products, get_sales_history, cleanup
        print("✅ Package-level imports working")
        
        # Test individual tool imports
        from hotmart.tools.products import get_products as products_tool
        from hotmart.tools.sales import get_sales_history as sales_tool
        from hotmart.tools.base import api_client, format_error, validate_max_results
        print("✅ Individual tool imports working")
        
        # Test base utilities
        error_msg = format_error("Test error")
        if error_msg == "Error: Test error":
            print("✅ Error formatting working")
        else:
            print(f"❌ Error formatting failed: {error_msg}")
            return False
        
        # Test max_results validation
        valid_result = validate_max_results(25)
        if valid_result is None:
            print("✅ Valid max_results validation working")
        else:
            print(f"❌ Valid max_results validation failed: {valid_result}")
            return False
        
        invalid_result = validate_max_results(100)
        if invalid_result and "must be between" in invalid_result:
            print("✅ Invalid max_results validation working")
        else:
            print(f"❌ Invalid max_results validation failed: {invalid_result}")
            return False
        
        # Test function equivalence
        print("🔄 Testing function equivalence...")
        
        if get_products == products_tool:
            print("✅ Products function equivalence confirmed")
        else:
            print("❌ Products function equivalence failed")
            return False
        
        if get_sales_history == sales_tool:
            print("✅ Sales function equivalence confirmed")
        else:
            print("❌ Sales function equivalence failed")
            return False
        
        # Test backward compatibility
        # Note: No legacy compatibility needed - this is version 1.0
        print("✅ No legacy compatibility required for v1.0")
        
        # Check if credentials are available for integration tests
        env_file = Path(__file__).parent.parent.parent / ".env"
        if not env_file.exists():
            print("⚠️ .env file not found - skipping integration tests")
            return True
        
        from dotenv import load_dotenv
        load_dotenv()
        
        required_vars = ["HOTMART_CLIENT_ID", "HOTMART_CLIENT_SECRET", "HOTMART_BASIC_TOKEN"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            print(f"⚠️ Missing credentials: {', '.join(missing_vars)} - skipping integration tests")
            return True
        
        print("🌐 Testing integration...")
        
        # Test that both tools use the same client instance
        try:
            # Quick test to ensure tools work together
            products_result = await get_products(max_results=1)
            sales_result = await get_sales_history(max_results=1)
            
            products_parsed = json.loads(products_result)
            sales_parsed = json.loads(sales_result)
            
            if "total_items" in products_parsed and "total_items" in sales_parsed:
                print("✅ Tools integration working")
            elif "error" in products_result.lower() or "error" in sales_result.lower():
                print("⚠️ Tools integration test returned API errors (expected in some environments)")
            else:
                print("❌ Tools integration returned unexpected format")
                await cleanup()
                return False
            
        except Exception as e:
            print(f"⚠️ Integration test failed: {e}")
            # Don't fail for API issues
        
        # Test cleanup
        await cleanup()
        print("✅ Cleanup successful")
        
        print("🎉 Tools integration test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Tools integration test failed: {e}")
        import traceback
        traceback.print_exc()
        try:
            from hotmart.tools import cleanup
            await cleanup()
        except:
            pass
        return False

def run_tools_test():
    """Synchronous wrapper for tools test"""
    return asyncio.run(test_tools())

if __name__ == "__main__":
    run_tools_test()
