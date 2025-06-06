#!/usr/bin/env python3
"""
POC: MCP Server SSE Tools Discovery
Conecta a um MCP server via SSE e retorna as tools disponíveis
"""

import asyncio
import json
import httpx
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from urllib.parse import urljoin

@dataclass
class MCPServerConfig:
    """Configuração para conectar ao MCP Server"""
    base_url: str
    port: int = 8000
    auth_token: Optional[str] = None
    timeout: int = 5  # Reduzido para 5 segundos
    
    @property
    def sse_url(self) -> str:
        return f"{self.base_url}:{self.port}/sse"

class MCPToolsDiscovery:
    """Cliente para descobrir tools em MCP Server via SSE"""
    
    def __init__(self, config: MCPServerConfig):
        self.config = config
        self.client = httpx.AsyncClient(timeout=config.timeout)
        
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    def _get_headers(self) -> Dict[str, str]:
        """Monta headers para requisições"""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        if self.config.auth_token:
            headers["Authorization"] = f"Bearer {self.config.auth_token}"
            
        return headers
    
    async def check_server_health(self) -> bool:
        """Verifica se o server SSE está respondendo (com timeout curto)"""
        try:
            # Usa timeout muito curto para não travar
            async with httpx.AsyncClient(timeout=2.0) as quick_client:
                # Faz HEAD request para ser mais rápido
                response = await quick_client.head(
                    self.config.sse_url, 
                    headers=self._get_headers()
                )
                # Aceita 200, 405 (Method Not Allowed) ou até 404
                return response.status_code in [200, 405, 404]
        except Exception as e:
            print(f"⚠️  Não foi possível verificar saúde (continuando mesmo assim): {e}")
            return True  # Assume que está OK e continua
    
    async def discover_tools_via_mcp_protocol(self) -> List[Dict[str, Any]]:
        """Descobre tools via protocolo MCP puro sobre SSE"""
        try:
            # Requisição MCP para listar tools
            mcp_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/list",
                "params": {}
            }
            
            # Envia requisição MCP via POST
            response = await self.client.post(
                self.config.sse_url,
                headers=self._get_headers(),
                json=mcp_request
            )
            
            if response.status_code == 200:
                data = response.json()
                if "result" in data and "tools" in data["result"]:
                    return data["result"]["tools"]
            
            return []
            
        except Exception as e:
            print(f"Erro ao descobrir tools via protocolo MCP: {e}")
            return []
    
    async def call_mcp_method(self, method: str, params: Dict = None) -> Optional[Dict[str, Any]]:
        """Chama qualquer método MCP e retorna a resposta"""
        try:
            mcp_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": method,
                "params": params or {}
            }
            
            response = await self.client.post(
                self.config.sse_url,
                headers=self._get_headers(),
                json=mcp_request
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Erro na chamada MCP {method}: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Erro ao chamar método MCP {method}: {e}")
            return None

def format_tools_output(tools: List[Dict[str, Any]]) -> str:
    """Formata a saída das tools descobertas"""
    if not tools:
        return "❌ Nenhuma tool encontrada"
    
    output = f"🔧 {len(tools)} tool(s) encontrada(s):\n\n"
    
    for i, tool in enumerate(tools, 1):
        name = tool.get("name", "N/A")
        description = tool.get("description", "Sem descrição")
        
        output += f"{i}. **{name}**\n"
        output += f"   📝 {description}\n"
        
        # Mostra parâmetros se existirem
        if "inputSchema" in tool:
            schema = tool["inputSchema"]
            if "properties" in schema:
                props = list(schema["properties"].keys())
                output += f"   🔑 Parâmetros: {', '.join(props)}\n"
        
        output += "\n"
    
    return output

async def main():
    """Função principal da POC"""
    
    # Configuração para seu servidor Hotmart MCP
    config = MCPServerConfig(
        base_url="http://127.0.0.1",
        port=8000,
        auth_token=None
    )
    
    print("🚀 POC: MCP Server SSE Tools Discovery")
    print(f"📡 Conectando em: {config.sse_url}\n")
    
    async with MCPToolsDiscovery(config) as discovery:
        
        # 1. Verificação rápida (ou pula se der problema)
        print("🏥 Verificação rápida do endpoint...")
        is_healthy = await discovery.check_server_health()
        
        if is_healthy:
            print("✅ Endpoint parece estar online")
        else:
            print("⚠️  Verificação falhou, mas vamos tentar mesmo assim...")
        
        # 2. Vai direto para o teste principal
        print("🔍 Descobrindo tools via protocolo MCP...")
        tools = await discovery.discover_tools_via_mcp_protocol()
        
        if tools:
            print("✅ Tools descobertas:")
            print(format_tools_output(tools))
            
            # 3. Testa uma tool específica se houver
            if tools:
                first_tool = tools[0]["name"]
                print(f"🧪 Testando informações da tool '{first_tool}'...")
                
                # Chama tools/call para ver se responde (sem argumentos)
                result = await discovery.call_mcp_method("tools/call", {
                    "name": first_tool,
                    "arguments": {}
                })
                
                if result:
                    if "result" in result:
                        print(f"✅ Tool respondeu: {result['result']}")
                    elif "error" in result:
                        print(f"⚠️  Tool retornou erro: {result['error']}")
                    else:
                        print(f"✅ Tool respondeu: {result}")
                else:
                    print("⚠️ Tool não respondeu")
        else:
            print("❌ Nenhuma tool encontrada")
            
            # 4. Debug: tenta initialize para ver se server responde
            print("\n🔧 Testando inicialização MCP...")
            
            server_info = await discovery.call_mcp_method("initialize", {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "tools-discovery-poc", "version": "1.0.0"}
            })
            
            if server_info:
                print(f"ℹ️  Servidor respondeu ao initialize: {server_info}")
            else:
                print("❌ Servidor não respondeu ao initialize")
        
        print("\n" + "="*50)
        print("POC concluída!")

if __name__ == "__main__":
    asyncio.run(main())