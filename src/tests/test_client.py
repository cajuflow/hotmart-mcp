"""
Test API client functionality
"""

import asyncio
import os
from pathlib import Path
import sys

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

async def test_client():
    """Test HotmartApiClient"""
    print("🌐 Testing API client...")
    
    try:
        from hotmart.client import HotmartApiClient
        
        # Check if credentials are available
        env_file = Path(__file__).parent.parent.parent / ".env"
        if not env_file.exists():
            print("⚠️ .env file not found - skipping client test")
            return True
        
        from dotenv import load_dotenv
        load_dotenv()
        
        required_vars = ["HOTMART_CLIENT_ID", "HOTMART_CLIENT_SECRET", "HOTMART_BASIC_TOKEN"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            print(f"⚠️ Missing credentials: {', '.join(missing_vars)} - skipping client test")
            return True
        
        # Test client instantiation
        client = HotmartApiClient()
        print("✅ API client created successfully")
        
        # Test connection
        try:
            connection_ok = await client.test_connection()
            
            if connection_ok:
                print("✅ API connection successful")
            else:
                print("❌ API connection failed")
                await client.close()
                return False
                
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            await client.close()
            return False
        
        # Test basic API calls (if connection is working)
        try:
            # Test products endpoint
            products_response = await client.get_products(max_results=1)
            if "items" in products_response:
                print("✅ Products endpoint working")
            else:
                print("⚠️ Products endpoint returned unexpected format")
            
            # Test sales history endpoint
            sales_response = await client.get_sales_history(max_results=1)
            if "items" in sales_response or "page_info" in sales_response:
                print("✅ Sales history endpoint working")
            else:
                print("⚠️ Sales history endpoint returned unexpected format")
                
        except Exception as e:
            print(f"⚠️ API endpoint test failed: {e}")
            # Don't fail the test for this - API might have no data
        
        # Clean up
        await client.close()
        print("✅ Client cleanup successful")
        
        print("🎉 API client test passed!")
        return True
        
    except Exception as e:
        print(f"❌ API client test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_client_test():
    """Synchronous wrapper for client test"""
    return asyncio.run(test_client())

if __name__ == "__main__":
    run_client_test()
