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

# Host e Porta para SSE Transport
MCP_HOST=0.0.0.0
MCP_PORT=8000
```

## ⚙️ Configuração Avançada

### Host e Porta do Servidor

Para uso com **Docker** ou **SSE transport**, configure:

```env
# Docker/Container (aceita conexões externas)
MCP_HOST=0.0.0.0
MCP_PORT=8000

# Local apenas (default)
MCP_HOST=127.0.0.1
MCP_PORT=8000
```

**Uso comum por ambiente:**
- **Local/STDIO**: `MCP_HOST=127.0.0.1` (padrão)
- **Docker/Container**: `MCP_HOST=0.0.0.0` (obrigatório)
- **Cloud/Produção**: `MCP_HOST=0.0.0.0` (recomendado)

### Configuração Alternativa via FastMCP

Você também pode usar variáveis de ambiente com prefixo `FASTMCP_`:

```env
# Alternativa à configuração MCP_HOST/MCP_PORT
FASTMCP_HOST=0.0.0.0
FASTMCP_PORT=8000
```

**Prioridade de configuração:**
1. 📜 Parâmetros no construtor do FastMCP (`MCP_HOST/MCP_PORT`)
2. 🌍 Variáveis de ambiente `FASTMCP_HOST/FASTMCP_PORT`
3. 📝 Arquivo `.env`
4. ⚙️ Padrões do FastMCP (`127.0.0.1:8000`)

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

### 6. Docker (Opcional)

```bash
# Build da imagem
docker build -t hotmart-mcp .

# Executar container (usa .env automático)
docker run -p 8000:8000 --env-file .env hotmart-mcp

# Testar conectividade
curl http://localhost:8000/sse
```

**Importante**: Para Docker, certifique-se que `MCP_HOST=0.0.0.0` no `.env`!

**Log esperado (Docker funcionando):**
```
-> Running in SSE mode on 0.0.0.0:8000
INFO:     Uvicorn running on http://0.0.0.0:8000
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
