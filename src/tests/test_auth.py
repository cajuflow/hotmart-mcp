"""
Test authentication functionality
"""

import asyncio
import os
from pathlib import Path
import sys

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

async def test_auth():
    """Test authentication service"""
    print("🔐 Testing authentication...")
    
    try:
        from hotmart.auth import AuthService
        
        # Check if credentials are available
        env_file = Path(__file__).parent.parent.parent / ".env"
        if not env_file.exists():
            print("⚠️ .env file not found - skipping auth test")
            return True
        
        from dotenv import load_dotenv
        load_dotenv()
        
        required_vars = ["HOTMART_CLIENT_ID", "HOTMART_CLIENT_SECRET", "HOTMART_BASIC_TOKEN"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            print(f"⚠️ Missing credentials: {', '.join(missing_vars)} - skipping auth test")
            return True
        
        # Test AuthService instantiation
        auth_service = AuthService()
        print("✅ AuthService created successfully")
        
        # Test token request
        try:
            token = await auth_service.get_access_token()
            
            if isinstance(token, str) and token:
                print("✅ Token obtained successfully")
                print(f"📝 Token (first 20 chars): {token[:20]}...")
                
                # Test token validation method exists
                is_valid = auth_service.is_token_valid()
                print(f"✅ Token validation method working: {is_valid}")
                
                # Test that we have internal token data
                if auth_service.access_token and auth_service.token_expires_at:
                    print("✅ Internal token state properly set")
                else:
                    print("❌ Internal token state not properly set")
                    await auth_service.close()
                    return False
                
            else:
                print(f"❌ Invalid token received: {type(token)} - {token}")
                await auth_service.close()
                return False
                
        except Exception as e:
            print(f"❌ Token request failed: {e}")
            await auth_service.close()
            return False
        
        # Clean up
        await auth_service.close()
        print("✅ AuthService cleanup successful")
        
        print("🎉 Authentication test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Authentication test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_auth_test():
    """Synchronous wrapper for auth test"""
    return asyncio.run(test_auth())

if __name__ == "__main__":
    run_auth_test()
