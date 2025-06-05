# Hotmart MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Model Context Protocol (MCP) server for integrating with Hotmart APIs. This server enables AI agents to manage products, sales, and other Hotmart operations through a standardized interface.

## 🏗️ Architecture

This project follows **modular architecture** with separation of concerns:

```
src/hotmart/
├── models/
│   ├── base.py         # 📋 ApiResponse, AuthToken
│   ├── product.py      # 📦 Product models
│   ├── sale.py         # 💰 Sale models
│   ├── subscription.py # 🔄 Subscription models
│   └── __init__.py     # 📚 Centralized imports
├── tools/
│   ├── base.py         # 🛠️ Utilities & validation
│   ├── products.py     # 📦 get_products tool
│   ├── sales.py        # 💰 get_sales tool
│   └── __init__.py     # 📚 Centralized imports
├── config.py           # ⚙️ Configuration
├── auth.py             # 🔐 Authentication
├── client.py           # 🌐 API client
└── __init__.py         # 📦 Package init

hotmart_mcp.py         # 🚀 MCP Server (main)
test.py               # 🧪 Architecture Testing
```

### Benefits:
- ✅ **Single Responsibility**: Each file has one clear purpose
- ✅ **Easy Maintenance**: Bug fixes isolated to specific components
- ✅ **Better Testing**: Components can be tested independently
- ✅ **Extensibility**: Add features without affecting existing code
- ✅ **Reusability**: Components can be used across projects

## 📦 Installation

### Prerequisites
- Python 3.11 or higher
- A Hotmart account with API credentials

### Setup

1. Clone the repository:
```bash
git clone https://github.com/cajuflow/hotmart-mcp.git
cd hotmart-mcp
```

2. Install with uv (recommended):
```bash
uv sync
```

Or with pip:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your Hotmart credentials
```

## 🔧 Configuration

Create a `.env` file with your Hotmart API credentials:

```env
HOTMART_CLIENT_ID=your_client_id_here
HOTMART_CLIENT_SECRET=your_client_secret_here
HOTMART_ENVIRONMENT=sandbox
```

### Getting Hotmart API Credentials

1. Log in to your Hotmart account
2. Go to **Manage my business** > **Products** > **Tools**
3. Click on **Hotmart Credentials**
4. Click **Create Credential**
5. Select **API Hotmart** and click **Create Credential**
6. **IMPORTANT**: Copy all three values:
   - **Client ID**
   - **Client Secret** 
   - **Basic Token** (this is essential for authentication!)

> ⚠️ **Note**: The Basic Token is required for authentication. Without it, you'll get 401 errors.

## 🔌 Claude Desktop Integration

To use this MCP server with Claude Desktop, add the following to your `claude_desktop_config.json`:

### Windows
```json
{
  "mcpServers": {
    "hotmart": {
      "command": "uv",
      "args": [
      "--directory",
      "F:\\src\\github\\cajuflow\\mcp\\hotmart-mcp",
      "run", "python", "hotmart_mcp.py"
      ]
    }
  }
}
```

### macOS/Linux
```json
{
  "mcpServers": {
    "hotmart": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/hotmart-mcp",
        "run",
        "python",
        "hotmart_mcp.py"
      ]
    }
  }
}
```

## 🛠️ Available Tools

### `get_products`
Lists all products from your Hotmart account.

**Parameters:**
- `status` (optional): Filter by product status (`ACTIVE`, `INACTIVE`, `DRAFT`)
- `limit` (optional): Number of products to return (default: 20, max: 100)
- `offset` (optional): Pagination offset (default: 0)

**Example usage in Claude:**
```
"List my active products from Hotmart"
"Show me the first 10 products"
"Get all inactive products"
```

## 🧪 Testing

### Quick Test
```bash
# Test the complete setup and architecture
uv run python test.py
```

### Manual Testing
```bash
# Run the MCP server
uv run python hotmart_mcp.py
```

## 🔧 Troubleshooting

### Common Issues

#### 401 Unauthorized Error
- **Cause**: Missing or incorrect Basic Token
- **Solution**: Ensure you have all 3 credentials from Hotmart:
  ```env
  HOTMART_CLIENT_ID=your_client_id
  HOTMART_CLIENT_SECRET=your_client_secret
  HOTMART_BASIC_TOKEN=your_basic_token  # This is crucial!
  ```

#### "FastMCP object has no attribute 'run_server'" Error
- **Cause**: Outdated MCP SDK
- **Solution**: Update dependencies:
  ```bash
  uv sync --upgrade
  ```

#### Claude Desktop Not Detecting Server
- **Cause**: Incorrect path in config
- **Solution**: Use absolute path in `claude_desktop_config.json`:
  ```json
  {
    "mcpServers": {
      "hotmart": {
        "command": "uv",
        "args": [
          "--directory",
          "F:\\src\\github\\cajuflow\\mcp\\hotmart-mcp",
          "run", "python", "hotmart_mcp.py"
        ]
      }
    }
  }
  ```

#### No Products Returned
- **Cause**: Empty product catalog or incorrect environment
- **Solution**: 
  - Check if you have products in your Hotmart account
  - Verify HOTMART_ENVIRONMENT (sandbox vs production)
  - Test with different status filters

### Debug Tools

```bash
# Complete system test
uv run python test.py

# Enable detailed logging
export LOG_LEVEL=DEBUG
uv run python hotmart_mcp.py
```

### Code Formatting

```bash
# Format code
uv run black hotmart_mcp.py

# Sort imports
uv run isort hotmart_mcp.py

# Type checking
uv run mypy hotmart_mcp.py
```

## 📋 API Reference

### Product Object Structure

```python
{
    "id": "12345",
    "name": "My Digital Course",
    "status": "ACTIVE",
    "type": "COURSE",
    "price": 99.99,
    "currency": "BRL",
    "created_date": "2025-01-01T00:00:00Z",
    "updated_date": "2025-01-15T00:00:00Z",
    "description": "Course description",
    "category": "Education"
}
```

## 🔒 Security

- All API calls use OAuth 2.0 authentication
- Credentials are stored in environment variables
- Tokens are automatically refreshed when expired
- Sandbox environment available for testing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📧 Email: support@cajuflow.com
- 💬 Discord: [Join our community](https://discord.gg/cajuflow)
- 🐛 Bug Reports: [GitHub Issues](https://github.com/cajuflow/hotmart-mcp/issues)

## 🔗 Related Projects

- [@cajuflow/cortaposta](https://github.com/cajuflow/cortaposta) - Automated video content creation
- [Cajuflow Automation Suite](https://cajuflow.com) - Complete automation solutions

---

**Made with ❤️ by [Cajuflow](https://cajuflow.com)**

*Empowering digital creators with intelligent automation solutions.*
