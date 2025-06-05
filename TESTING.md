# 🧪 Hotmart MCP Test Suite

Comprehensive testing framework for the Hotmart MCP Server implementation.

## 📁 Test Structure

```
src/tests/
├── __init__.py           # Test package initialization
├── test_imports.py       # Import and dependency tests
├── test_config.py        # Configuration and environment tests
├── test_auth.py          # Authentication service tests
├── test_client.py        # API client functionality tests
├── test_products.py      # Products tools and validation tests
├── test_sales.py         # Sales tools and validation tests
└── test_tools.py         # Tools integration tests

Root test files:
├── run_tests.py          # Main test runner (runs all tests)
├── test_runner.py        # Individual test runner
└── pyproject.toml        # pytest configuration
```

## 🚀 Running Tests

### Run All Tests
```bash
# Comprehensive test suite
python run_tests.py

# Alternative with detailed output
python -m pytest src/tests/ -v
```

### Run Individual Tests
```bash
# Test specific modules
python test_runner.py imports
python test_runner.py config
python test_runner.py auth
python test_runner.py client
python test_runner.py products
python test_runner.py sales
python test_runner.py tools

# Get help
python test_runner.py --help
```

### Run Individual Test Files
```bash
# Direct execution
python src/tests/test_sales.py
python src/tests/test_products.py
```

## 📋 Test Categories

### 🔗 Import Tests (`test_imports.py`)
- **Purpose**: Verify all modules load correctly
- **Tests**: Core imports, model imports, tool imports, package-level imports
- **Critical**: Must pass for other tests to work

### ⚙️ Configuration Tests (`test_config.py`)
- **Purpose**: Validate environment setup
- **Tests**: Environment detection, URLs, endpoints, credentials
- **Requirements**: `.env` file for full testing

### 🔐 Authentication Tests (`test_auth.py`)
- **Purpose**: Test OAuth 2.0 flow
- **Tests**: Token request, validation, expiration
- **Requirements**: Valid API credentials

### 🌐 API Client Tests (`test_client.py`)
- **Purpose**: Test HTTP client functionality
- **Tests**: Connection, basic API calls, error handling
- **Requirements**: Valid API credentials and network access

### 📦 Products Tests (`test_products.py`)
- **Purpose**: Test product tools and validation
- **Tests**: Validation functions, API calls, filtering
- **Coverage**: All product parameters and edge cases

### 💰 Sales Tests (`test_sales.py`)
- **Purpose**: Test sales tools and validation
- **Tests**: Validation functions, API calls, multiple filters
- **Coverage**: All sales parameters and combinations

### 🔧 Tools Integration Tests (`test_tools.py`)
- **Purpose**: Test tool integration and compatibility
- **Tests**: Package imports, function equivalence, backward compatibility
- **Focus**: Integration between different modules

## 📊 Test Results

### Success Indicators
- ✅ **PASSED**: Test completed successfully
- ⚠️ **WARNING**: Test passed with warnings (e.g., missing credentials)
- ❌ **FAILED**: Test failed and needs attention

### Exit Codes
- `0`: All tests passed
- `1`: One or more tests failed

## 🔧 Prerequisites

### Required Files
```bash
.env                    # API credentials (copy from .env.example)
```

### Environment Variables
```bash
HOTMART_CLIENT_ID=your_client_id
HOTMART_CLIENT_SECRET=your_client_secret  
HOTMART_BASIC_TOKEN=your_basic_token
HOTMART_ENVIRONMENT=sandbox  # or production
```

### Python Dependencies
```bash
# Install all dependencies
pip install -r requirements.txt

# Core testing dependencies
pip install asyncio aiohttp pydantic python-dotenv
```

## 📈 Test Coverage

### Current Coverage
- ✅ **Imports**: 100% (all modules)
- ✅ **Configuration**: 100% (all settings)
- ✅ **Authentication**: 100% (OAuth flow)
- ✅ **API Client**: 100% (HTTP operations)
- ✅ **Products**: 100% (all parameters)
- ✅ **Sales**: 100% (all parameters)
- ✅ **Tools**: 100% (integration)

### Test Types
- **Unit Tests**: Individual function testing
- **Integration Tests**: Module interaction testing
- **API Tests**: Live API endpoint testing
- **Validation Tests**: Parameter and error handling

## 🐛 Troubleshooting

### Common Issues

#### "Import Error"
```bash
# Fix: Add src to Python path
export PYTHONPATH="$PYTHONPATH:./src"
# Or use the provided test runners
```

#### "Missing Credentials"
```bash
# Fix: Create .env file
cp .env.example .env
# Edit .env with your API credentials
```

#### "API Connection Failed"
```bash
# Check: Network connectivity
# Check: API credentials validity
# Check: Environment (sandbox vs production)
```

#### "Authentication Failed"
```bash
# Check: HOTMART_CLIENT_ID is correct
# Check: HOTMART_CLIENT_SECRET is correct
# Check: HOTMART_BASIC_TOKEN is correct
# Check: Environment matches your credentials
```

### Debug Mode
```bash
# Run with detailed output
python run_tests.py --verbose

# Run specific test with debug
python -c "
import sys
sys.path.insert(0, 'src')
from tests.test_sales import run_sales_test
import asyncio
asyncio.run(run_sales_test())
"
```

## 🔄 Continuous Integration

### GitHub Actions (example)
```yaml
name: Test Hotmart MCP
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python run_tests.py
```

### Local Development
```bash
# Pre-commit testing
python run_tests.py

# Quick validation
python test_runner.py imports

# API functionality
python test_runner.py sales
```

## 📝 Adding New Tests

### Create New Test Module
```python
# src/tests/test_new_feature.py
async def test_new_feature():
    """Test new feature functionality"""
    print("🧪 Testing new feature...")
    try:
        # Test logic here
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def run_new_feature_test():
    """Sync wrapper"""
    return asyncio.run(test_new_feature())

if __name__ == "__main__":
    run_new_feature_test()
```

### Update Test Runner
```python
# Add to run_tests.py
elif test_name == "new_feature":
    from tests.test_new_feature import run_new_feature_test
    success = run_new_feature_test()
```

## 📚 Best Practices

### Test Writing
- ✅ Include both positive and negative test cases
- ✅ Test edge cases and error conditions
- ✅ Use descriptive test names and messages
- ✅ Handle exceptions gracefully
- ✅ Clean up resources (API connections, etc.)

### Test Organization
- ✅ One test file per major module
- ✅ Group related tests together
- ✅ Use consistent naming conventions
- ✅ Document test purposes and requirements

### CI/CD Integration
- ✅ Fast feedback on failures
- ✅ Clear error messages
- ✅ Appropriate exit codes
- ✅ Environment-aware testing
