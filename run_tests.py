#!/usr/bin/env python3
"""
Hotmart MCP Test Suite - Main Test Runner
Executes all tests in the correct order and provides comprehensive reporting
"""

import asyncio
import sys
import time
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Test results tracking
test_results = {}
total_tests = 0
passed_tests = 0

def print_header():
    """Print test suite header"""
    print("🧪 HOTMART MCP TEST SUITE")
    print("=" * 60)
    print("🚀 Running comprehensive tests for Hotmart MCP Server")
    print("📋 Testing: Imports, Config, Auth, Client, Products, Sales, Tools")
    print("=" * 60)

def print_test_separator(test_name):
    """Print separator for each test"""
    print(f"\n{'─' * 20} {test_name.upper()} {'─' * 20}")

def record_test_result(test_name, success):
    """Record test result"""
    global total_tests, passed_tests
    total_tests += 1
    if success:
        passed_tests += 1
    test_results[test_name] = "✅ PASSED" if success else "❌ FAILED"

async def run_all_tests():
    """Run all tests in the correct order"""
    print_header()
    start_time = time.time()
    
    # 1. Test Imports
    print_test_separator("IMPORTS TEST")
    try:
        from tests.test_imports import test_imports
        success = test_imports()
        record_test_result("Imports", success)
        if not success:
            print("🛑 Critical failure: Cannot proceed without proper imports")
            return False
    except Exception as e:
        print(f"❌ Critical error in imports test: {e}")
        record_test_result("Imports", False)
        return False
    
    # 2. Test Configuration
    print_test_separator("CONFIGURATION TEST")
    try:
        from tests.test_config import test_config
        success = test_config()
        record_test_result("Configuration", success)
        if not success:
            print("⚠️ Configuration issues detected - some tests may fail")
    except Exception as e:
        print(f"❌ Configuration test error: {e}")
        record_test_result("Configuration", False)
    
    # 3. Test Authentication
    print_test_separator("AUTHENTICATION TEST")
    try:
        from tests.test_auth import test_auth
        success = await test_auth()  # Chamada direta da função async
        record_test_result("Authentication", success)
    except Exception as e:
        print(f"❌ Authentication test error: {e}")
        record_test_result("Authentication", False)
    
    # 4. Test API Client
    print_test_separator("API CLIENT TEST")
    try:
        from tests.test_client import test_client
        success = await test_client()  # Chamada direta da função async
        record_test_result("API Client", success)
    except Exception as e:
        print(f"❌ API Client test error: {e}")
        record_test_result("API Client", False)
    
    # 5. Test Products
    print_test_separator("PRODUCTS TEST")
    try:
        from tests.test_products import test_products
        success = await test_products()  # Chamada direta da função async
        record_test_result("Products", success)
    except Exception as e:
        print(f"❌ Products test error: {e}")
        record_test_result("Products", False)
    
    # 6. Test Sales
    print_test_separator("SALES TEST")
    try:
        from tests.test_sales import test_sales
        success = await test_sales()  # Chamada direta da função async
        record_test_result("Sales", success)
    except Exception as e:
        print(f"❌ Sales test error: {e}")
        record_test_result("Sales", False)
    
    # 7. Test Tools Integration
    print_test_separator("TOOLS INTEGRATION TEST")
    try:
        from tests.test_tools import test_tools
        success = await test_tools()  # Chamada direta da função async
        record_test_result("Tools Integration", success)
    except Exception as e:
        print(f"❌ Tools integration test error: {e}")
        record_test_result("Tools Integration", False)
    
    # Calculate test duration
    end_time = time.time()
    duration = end_time - start_time
    
    # Print final results
    print_final_results(duration)
    
    return passed_tests == total_tests

def print_final_results(duration):
    """Print comprehensive test results"""
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    # Individual test results
    for test_name, result in test_results.items():
        print(f"{result} {test_name}")
    
    print("-" * 60)
    
    # Overall statistics
    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    print(f"📈 OVERALL RESULTS: {passed_tests}/{total_tests} tests passed ({success_rate:.1f}%)")
    print(f"⏱️ DURATION: {duration:.2f} seconds")
    
    # Status message
    if passed_tests == total_tests:
        print("\n🎉 ALL TESTS PASSED! Your Hotmart MCP is ready for production!")
        print("\n🚀 Next steps:")
        print("   1. Run: python hotmart_mcp.py (to start the server)")
        print("   2. Configure Claude Desktop with your server")
        print("   3. Test with Claude interface")
        print("   4. Implement additional features (Subscriptions, Analytics)")
    elif passed_tests >= total_tests * 0.8:
        print("\n✅ MOSTLY SUCCESSFUL! Minor issues detected.")
        print("⚠️ Check failed tests above - they might be due to:")
        print("   • Missing .env configuration")
        print("   • Network connectivity issues")
        print("   • API rate limits or permissions")
    else:
        print("\n❌ SIGNIFICANT ISSUES DETECTED!")
        print("🔧 Please fix the following before proceeding:")
        print("   • Critical import or configuration errors")
        print("   • Authentication problems")
        print("   • Missing dependencies")
    
    print("\n📋 Test Categories:")
    print("   🔗 Imports: Core module loading and dependencies")
    print("   ⚙️ Configuration: Environment setup and settings")
    print("   🔐 Authentication: OAuth 2.0 token management")
    print("   🌐 API Client: HTTP client and connection testing")
    print("   📦 Products: Product listing and filtering")
    print("   💰 Sales: Sales history and transaction data")
    print("   🔧 Tools: Integration and package-level functionality")

def check_environment():
    """Check if environment is properly set up"""
    print("🔍 Pre-flight environment check...")
    
    # Check if .env exists
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️ .env file not found")
        print("📝 To run full tests:")
        print("   1. Copy .env.example to .env")
        print("   2. Configure your Hotmart API credentials")
        print("   3. Re-run tests")
        print("\n🔄 Running tests without API credentials...")
        return False
    else:
        print("✅ .env file found")
        return True

async def main():
    """Main test runner"""
    # Check environment
    has_credentials = check_environment()
    
    if not has_credentials:
        print("\n📋 Note: Some tests will be skipped without API credentials")
        print("🧪 Running structural and validation tests only...")
    
    # Run all tests
    success = await run_all_tests()
    
    # Exit with appropriate code
    exit_code = 0 if success else 1
    
    if success:
        print(f"\n✅ Test suite completed successfully! (exit code: {exit_code})")
    else:
        print(f"\n❌ Test suite completed with failures! (exit code: {exit_code})")
    
    return exit_code

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
