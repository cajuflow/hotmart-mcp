#!/usr/bin/env python3
"""
Individual Test Runner - Run specific test modules
Usage: python test_runner.py [test_name]
Available tests: imports, config, auth, client, products, sales, tools
"""

import asyncio
import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def print_usage():
    """Print usage information"""
    print("🧪 Individual Test Runner")
    print("=" * 40)
    print("Usage: python test_runner.py [test_name]")
    print("\nAvailable tests:")
    print("  imports    - Test module imports and dependencies")
    print("  config     - Test configuration and environment")
    print("  auth       - Test authentication service")
    print("  client     - Test API client functionality")
    print("  products   - Test products tools and validation")
    print("  sales      - Test sales tools and validation")
    print("  tools      - Test tools integration")
    print("  all        - Run all tests (same as run_tests.py)")
    print("\nExamples:")
    print("  python test_runner.py sales")
    print("  python test_runner.py imports")
    print("  python test_runner.py all")

async def run_single_test(test_name):
    """Run a single test module"""
    test_name = test_name.lower()
    
    print(f"🧪 Running {test_name.upper()} test...")
    print("=" * 40)
    
    success = False
    
    try:
        if test_name == "imports":
            from tests.test_imports import test_imports
            success = test_imports()
            
        elif test_name == "config":
            from tests.test_config import test_config
            success = test_config()
            
        elif test_name == "auth":
            from tests.test_auth import test_auth
            success = await test_auth()  # Chamada direta da função async
            
        elif test_name == "client":
            from tests.test_client import test_client
            success = await test_client()  # Chamada direta da função async
            
        elif test_name == "products":
            from tests.test_products import test_products
            success = await test_products()  # Chamada direta da função async
            
        elif test_name == "sales":
            from tests.test_sales import test_sales
            success = await test_sales()  # Chamada direta da função async
            
        elif test_name == "tools":
            from tests.test_tools import test_tools
            success = await test_tools()  # Chamada direta da função async
            
        elif test_name == "all":
            # Import and run the main test suite
            import subprocess
            result = subprocess.run([sys.executable, "run_tests.py"], 
                                  capture_output=False, text=True)
            success = result.returncode == 0
            
        else:
            print(f"❌ Unknown test: {test_name}")
            print_usage()
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        success = False
    
    print("\n" + "=" * 40)
    if success:
        print(f"✅ {test_name.upper()} test PASSED!")
    else:
        print(f"❌ {test_name.upper()} test FAILED!")
    
    return success

def main():
    """Main runner"""
    if len(sys.argv) != 2:
        print_usage()
        return 1
    
    test_name = sys.argv[1]
    
    if test_name in ["-h", "--help", "help"]:
        print_usage()
        return 0
    
    # Run the test
    success = asyncio.run(run_single_test(test_name))
    
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
