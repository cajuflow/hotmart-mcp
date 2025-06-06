#!/usr/bin/env python3
"""
POC: MCP SSE Tools Discovery - POST + SSE Response Pattern
"""

import asyncio
import json
import httpx
import uuid
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

@dataclass
class MCPServerConfig:
    """Configuração para conectar ao MCP Server"""
    base_url: str
    port: int = 8000
    timeout: int = 15
    
    @property
    def sse_stream_url(self) -> str:
        return f"{self.base_url}:{self.port}/sse"
        
    @property
    def messages_url(self) -> str:
        return f"{self.base_url}:{self.port}/messages/"

class MCPSSEToolsClient:
    """Cliente que envia via POST e recebe via SSE simultaneamente"""
    
    def __init__(self, config: MCPServerConfig):
        self.config = config
        self.session_id = None
        self.client = httpx.AsyncClient(timeout=config.timeout)
        self.responses = {}
        self.request_id = 0
        self.sse_task = None
        self.sse_active = False
        
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.sse_task:
            self.sse_task.cancel()
        await self.client.aclose()
    
    def _get_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def _next_request_id(self) -> int:
        self.request_id += 1
        return self.request_id
    
    async def _listen_sse_responses(self):
        """Task dedicada para ouvir respostas via SSE"""
        try:
            print("🎧 Iniciando escuta de respostas SSE...")
            
            async with self.client.stream("GET", self.config.sse_stream_url) as response:
                if response.status_code != 200:
                    print(f"❌ Erro SSE: {response.status_code}")
                    return
                
                self.sse_active = True
                print("✅ Escuta SSE ativa!")
                
                async for line in response.aiter_lines():
                    if not self.sse_active:
                        break
                        
                    # Captura session_id se ainda não temos
                    if not self.session_id and "session_id=" in line:
                        session_start = line.find("session_id=") + 11
                        self.session_id = line[session_start:].strip()
                        print(f"📋 Session ID: {self.session_id}")
                        continue
                    
                    # Processa eventos de dados
                    if line.startswith("data: "):
                        try:
                            data_str = line[6:].strip()
                            if not data_str:
                                continue
                                
                            # Tenta parse JSON
                            data = json.loads(data_str)
                            
                            # Se tem ID, é resposta a requisição
                            if "id" in data:
                                req_id = data["id"]
                                self.responses[req_id] = data
                                method = data.get("method", "resultado")
                                print(f"📨 Resposta recebida para req {req_id}: {method}")
                            else:
                                print(f"📢 Evento: {data}")
                                
                        except json.JSONDecodeError:
                            # Ignora linhas não-JSON
                            continue
                
        except Exception as e:
            print(f"❌ Erro na escuta SSE: {e}")
        finally:
            self.sse_active = False
    
    async def _wait_for_session(self, max_wait: int = 5) -> bool:
        """Aguarda session_id ser capturado"""
        for _ in range(max_wait * 10):  # décimos de segundo
            if self.session_id:
                return True
            await asyncio.sleep(0.1)
        return False
    
    async def _send_and_wait(self, method: str, params: Dict = None, timeout: float = 8.0) -> Optional[Dict[str, Any]]:
        """Envia mensagem e aguarda resposta via SSE"""
        if not self.session_id:
            print("❌ Session ID não disponível")
            return None
            
        req_id = self._next_request_id()
        
        message = {
            "jsonrpc": "2.0",
            "id": req_id,
            "method": method,
            "params": params or {}
        }
        
        try:
            url_with_session = f"{self.config.messages_url}?session_id={self.session_id}"
            
            print(f"📤 Enviando {method} (id={req_id})")
            
            # Envia mensagem
            response = await self.client.post(
                url_with_session,
                headers=self._get_headers(),
                json=message
            )
            
            if response.status_code in [200, 202]:  # 202 = Accepted
                print(f"✅ Mensagem aceita (status {response.status_code})")
                
                # Aguarda resposta via SSE
                for _ in range(int(timeout * 10)):
                    if req_id in self.responses:
                        response_data = self.responses.pop(req_id)
                        return response_data
                    await asyncio.sleep(0.1)
                
                print(f"⏱️  Timeout aguardando resposta de {method}")
                return None
            else:
                print(f"❌ Erro HTTP {response.status_code}: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Erro enviando {method}: {e}")
            return None
    
    async def start_session(self) -> bool:
        """Inicia sessão SSE"""
        # Inicia task de escuta SSE
        self.sse_task = asyncio.create_task(self._listen_sse_responses())
        
        # Aguarda session_id ser capturado
        if not await self._wait_for_session():
            print("❌ Timeout aguardando session_id")
            return False
        
        print(f"✅ Sessão iniciada: {self.session_id}")
        return True
    
    async def initialize(self) -> bool:
        """Inicializa protocolo MCP"""
        print("\n🔌 Inicializando MCP...")
        
        response = await self._send_and_wait("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "clientInfo": {"name": "tools-discovery", "version": "1.0.0"}
        })
        
        if response and "result" in response:
            server_info = response["result"].get("serverInfo", {})
            print(f"✅ MCP inicializado!")
            print(f"   Servidor: {server_info.get('name', 'N/A')}")
            print(f"   Versão: {server_info.get('version', 'N/A')}")
            return True
        else:
            print("⚠️  Initialize falhou, continuando...")
            return False
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """Lista ferramentas disponíveis"""
        print("\n🔧 Listando tools...")
        
        response = await self._send_and_wait("tools/list")
        
        if response and "result" in response and "tools" in response["result"]:
            tools = response["result"]["tools"]
            print(f"✅ {len(tools)} tool(s) encontrada(s)!")
            return tools
        else:
            print("❌ Erro ao listar tools")
            if response and "error" in response:
                print(f"   Erro: {response['error']}")
            return []
    
    async def stop_session(self):
        """Para sessão SSE"""
        self.sse_active = False
        if self.sse_task:
            self.sse_task.cancel()

def format_tools_output(tools: List[Dict[str, Any]]) -> str:
    """Formata saída das tools"""
    if not tools:
        return "❌ Nenhuma tool encontrada"
    
    output = f"\n🎯 {len(tools)} TOOL(S) DESCOBERTA(S):\n" + "="*60 + "\n"
    
    for i, tool in enumerate(tools, 1):
        name = tool.get("name", "N/A")
        description = tool.get("description", "Sem descrição")
        
        output += f"\n{i}. 🔧 **{name}**\n"
        output += f"   📝 {description}\n"
        
        # Parâmetros
        if "inputSchema" in tool and "properties" in tool["inputSchema"]:
            props = tool["inputSchema"]["properties"]
            required = tool["inputSchema"].get("required", [])
            
            output += "   📋 Parâmetros:\n"
            for param_name, param_info in props.items():
                required_mark = " ⭐" if param_name in required else ""
                param_type = param_info.get("type", "")
                param_desc = param_info.get("description", "")
                output += f"      • {param_name}{required_mark} ({param_type}): {param_desc}\n"
        
        output += "\n" + "-"*50 + "\n"
    
    return output

async def main():
    """Função principal"""
    
    config = MCPServerConfig(
        base_url="http://127.0.0.1",
        port=8000
    )
    
    print("🚀 POC: MCP Tools Discovery via SSE")
    print(f"📡 Stream: {config.sse_stream_url}")
    print(f"💬 Messages: {config.messages_url}")
    print("="*60)
    
    async with MCPSSEToolsClient(config) as client:
        
        # 1. Inicia sessão SSE
        if not await client.start_session():
            print("❌ Falha ao iniciar sessão")
            return
        
        # 2. Inicializa protocolo
        await client.initialize()
        
        # 3. Lista tools (principal objetivo)
        tools = await client.list_tools()
        
        if tools:
            print(format_tools_output(tools))
            
            print("\n🎉 SUCESSO!")
            print(f"✅ Servidor MCP conectado via SSE")
            print(f"✅ {len(tools)} ferramenta(s) descoberta(s)")
            print(f"✅ Protocolo funcionando perfeitamente")
        else:
            print("\n❌ FALHA!")
            print("❌ Nenhuma tool descoberta")
        
        # 4. Para sessão
        await client.stop_session()
        
        print("\n" + "="*60)
        print("🎯 POC Concluída!")

if __name__ == "__main__":
    asyncio.run(main())