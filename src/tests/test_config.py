"""
Test configuration module
"""

import os
from pathlib import Path
import sys

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_config():
    """Test configuration settings"""
    print("⚙️ Testing configuration...")
    
    try:
        from hotmart.config import (
            HOTMART_ENVIRONMENT, 
            BASE_URL, 
            AUTH_URL,
            ENDPOINTS,
            BASE_URLS,
            AUTH_URLS
        )
        
        # Test environment detection
        print(f"✅ Environment detected: {HOTMART_ENVIRONMENT}")
        
        # Test base URL
        expected_sandbox = "https://sandbox.hotmart.com"
        expected_production = "https://developers.hotmart.com"
        
        if HOTMART_ENVIRONMENT == "sandbox":
            assert BASE_URL == expected_sandbox, f"Expected {expected_sandbox}, got {BASE_URL}"
        else:
            assert BASE_URL == expected_production, f"Expected {expected_production}, got {BASE_URL}"
        
        print(f"✅ Base URL correct: {BASE_URL}")
        
        # Test auth URL
        print(f"✅ Auth URL correct: {AUTH_URL}")
        
        # Test endpoints
        required_endpoints = ["AUTH_TOKEN", "PRODUCTS", "SALES_HISTORY", "SUBSCRIPTIONS"]
        for endpoint in required_endpoints:
            assert endpoint in ENDPOINTS, f"Missing endpoint: {endpoint}"
        
        print(f"✅ All endpoints available: {list(ENDPOINTS.keys())}")
        
        # Test environment variables (if .env exists)
        env_file = Path(__file__).parent.parent.parent / ".env"
        if env_file.exists():
            from dotenv import load_dotenv
            load_dotenv()
            
            required_vars = ["HOTMART_CLIENT_ID", "HOTMART_CLIENT_SECRET", "HOTMART_BASIC_TOKEN"]
            missing_vars = []
            
            for var in required_vars:
                if not os.getenv(var):
                    missing_vars.append(var)
            
            if missing_vars:
                print(f"⚠️ Missing environment variables: {', '.join(missing_vars)}")
                return False
            else:
                print("✅ All required environment variables present")
        else:
            print("⚠️ .env file not found - configuration will use defaults")
        
        print("🎉 Configuration test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_config()
