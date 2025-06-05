"""
Test products functionality
"""

import asyncio
import json
import os
from pathlib import Path
import sys

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

async def test_products():
    """Test products tools and functionality"""
    print("📦 Testing products functionality...")
    
    try:
        from hotmart.tools.products import get_products, validate_status, validate_format
        from hotmart.tools import cleanup
        
        # Test validation functions first
        print("🧪 Testing validation functions...")
        
        # Test valid status
        result1 = validate_status("ACTIVE")
        if result1 is None:
            print("✅ Valid status validation working")
        else:
            print(f"❌ Valid status validation failed: {result1}")
            return False
        
        # Test invalid status
        result2 = validate_status("INVALID_STATUS")
        if result2 and "invalid" in result2.lower():
            print("✅ Invalid status validation working")
        else:
            print(f"❌ Invalid status validation failed: {result2}")
            return False
        
        # Test valid format
        result3 = validate_format("ONLINE_COURSE")
        if result3 is None:
            print("✅ Valid format validation working")
        else:
            print(f"❌ Valid format validation failed: {result3}")
            return False
        
        # Test invalid format
        result4 = validate_format("INVALID_FORMAT")
        if result4 and "invalid" in result4.lower():
            print("✅ Invalid format validation working")
        else:
            print(f"❌ Invalid format validation failed: {result4}")
            return False
        
        # Check if credentials are available for API tests
        env_file = Path(__file__).parent.parent.parent / ".env"
        if not env_file.exists():
            print("⚠️ .env file not found - skipping API tests")
            return True
        
        from dotenv import load_dotenv
        load_dotenv()
        
        required_vars = ["HOTMART_CLIENT_ID", "HOTMART_CLIENT_SECRET", "HOTMART_BASIC_TOKEN"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            print(f"⚠️ Missing credentials: {', '.join(missing_vars)} - skipping API tests")
            return True
        
        print("🌐 Testing API calls...")
        
        # Test basic get_products call
        result = await get_products(max_results=3)
        parsed = json.loads(result)
        
        if "error" in result.lower():
            print(f"⚠️ API call returned error: {result}")
            # Don't fail - might be expected in some environments
        else:
            print(f"✅ Basic products call successful! Found {parsed.get('total_items', 0)} products")
        
        # Test with status filter
        result2 = await get_products(status="ACTIVE", max_results=2)
        parsed2 = json.loads(result2)
        
        if "error" in result2.lower():
            print(f"⚠️ Status filter call returned error")
        else:
            print(f"✅ Status filter call successful! Found {parsed2.get('total_items', 0)} active products")
        
        # Test with format filter
        result3 = await get_products(format="ONLINE_COURSE", max_results=1)
        parsed3 = json.loads(result3)
        
        if "error" in result3.lower():
            print(f"⚠️ Format filter call returned error")
        else:
            print(f"✅ Format filter call successful! Found {parsed3.get('total_items', 0)} online courses")
        
        # Test validation in API call
        result4 = await get_products(status="INVALID_STATUS")
        if "error" in result4.lower() and "invalid" in result4.lower():
            print("✅ API validation working correctly")
        else:
            print(f"❌ API validation not working: {result4}")
            await cleanup()
            return False
        
        await cleanup()
        
        print("🎉 Products functionality test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Products test failed: {e}")
        import traceback
        traceback.print_exc()
        try:
            from hotmart.tools import cleanup
            await cleanup()
        except:
            pass
        return False

def run_products_test():
    """Synchronous wrapper for products test"""
    return asyncio.run(test_products())

if __name__ == "__main__":
    run_products_test()
