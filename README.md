# Hotmart MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

Servidor MCP (Model Context Protocol) para integração com APIs da Hotmart. Este servidor permite que agentes de IA gerenciem produtos, vendas e outras operações da Hotmart através de uma interface padronizada.

## 📋 Sobre

O **Hotmart MCP Server** é uma implementação do Model Context Protocol que conecta o Claude (e outros LLMs) diretamente às APIs da Hotmart. Desenvolvido com arquitetura modular e suporte a múltiplos transportes (STDIO local e SSE web), oferece uma integração robusta e flexível para automação de operações de produtores digitais.

## 📋 Pré-requisitos

- **Python 3.11** ou superior
- **Conta Hotmart** com credenciais de API
- **uv** (recomendado) ou pip para gerenciamento de dependências
- **Claude Desktop** (para uso local) ou navegador web (para uso SSE)

## 🚀 Instalação

### 1. Clonar o Repositório
```bash
git clone https://github.com/cajuflow/hotmart-mcp.git
cd hotmart-mcp
```

### 2. Instalar Dependências
```bash
uv sync
```

### 3. Configurar Variáveis de Ambiente
```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar com suas credenciais
nano .env
```

Conteúdo do `.env`:
```env
# Credenciais Hotmart (obrigatório)
HOTMART_CLIENT_ID=seu_client_id_aqui
HOTMART_CLIENT_SECRET=seu_client_secret_aqui
HOTMART_BASIC_TOKEN=seu_basic_token_aqui

# Ambiente da Hotmart (sandbox ou production)
HOTMART_ENVIRONMENT=sandbox

# Configuração MCP (sse ou stdio)
TRANSPORT_TYPE=stdio
```

### 4. Integração com Claude Desktop

Adicione ao seu `claude_desktop_config.json`:

**stdio:**
```json
{
  "mcpServers": {
    "hotmart": {
      "command": "uv"
    }
  }
}
```

**sse:**
```json
{
  "mcpServers": {
    "hotmart": {
      "command": "uv", 
      "args": [
        "--directory",
        "/caminho/absoluto/para/hotmart-mcp",
        "run", "python", "hotmart_mcp.py"
      ]
    }
  }
}
```

### 5. Executar o Servidor

```bash
# Modo STDIO (padrão - Claude Desktop)
uv run python hotmart_mcp.py

# Modo SSE (aplicações web)
TRANSPORT_TYPE=sse uv run python hotmart_mcp.py
```

## 🛠️ Ferramentas Disponíveis

* `get_hotmart_products`: Lista produtos da sua conta Hotmart com filtros avançados.
* `get_hotmart_sales_history`: Obtém histórico de vendas com filtros detalhados.

### Testes
```bash
uv run python test_runner.py all
```


## 🆘 Suporte

- 📧 **Email**: contato@vdscruz.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/cajuflow/hotmart-mcp/issues)

---

**Desenvolvido com ❤️ pela Cajuflow**

*Empoderando criadores digitais com soluções inteligentes de automação.*
