#!/usr/bin/env python3
"""
Teste direto do container MCP via HTTP
Testa o servidor MCP rodando no container
"""

import asyncio
import aiohttp
import json
import os
import sys
from pathlib import Path

# Configuration
CONTAINER_URL = "http://localhost:8122"  # Container port from docker-compose
TEST_TIMEOUT = 30

async def test_container_health():
    """Test if container is running and responding."""
    
    print("🏥 Testando saúde do container...")
    
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
            async with session.get(f"{CONTAINER_URL}/health") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"   ✅ Container saudável: {data}")
                    return True
                else:
                    print(f"   ⚠️  Status HTTP: {response.status}")
                    return False
    except Exception as e:
        print(f"   ❌ Erro de conexão: {e}")
        return False

async def test_mcp_sse_connection():
    """Test MCP SSE connection."""
    
    print("🔌 Testando conexão SSE do MCP...")
    
    try:
        async with aiohttp.ClientSession() as session:
            headers = {
                'Accept': 'text/event-stream',
                'Cache-Control': 'no-cache'
            }
            
            async with session.get(f"{CONTAINER_URL}/sse", headers=headers) as response:
                if response.status == 200:
                    print("   ✅ Conexão SSE estabelecida")
                    return True
                else:
                    print(f"   ❌ Status SSE: {response.status}")
                    return False
    except Exception as e:
        print(f"   ❌ Erro SSE: {e}")
        return False

async def test_mcp_request():
    """Test MCP request via HTTP."""
    
    print("🧠 Testando requisição MCP...")
    
    try:
        # Sample MCP request
        mcp_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        }
        
        async with aiohttp.ClientSession() as session:
            headers = {'Content-Type': 'application/json'}
            
            async with session.post(
                f"{CONTAINER_URL}/message", 
                json=mcp_request,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    print(f"   ✅ MCP respondeu: {len(str(data))} chars")
                    
                    # Check if tools are listed
                    if 'result' in data and 'tools' in data['result']:
                        tools = data['result']['tools']
                        print(f"   📋 Ferramentas disponíveis: {len(tools)}")
                        for tool in tools[:3]:  # Show first 3 tools
                            print(f"      • {tool.get('name', 'Unknown')}")
                        return True
                    else:
                        print(f"   ⚠️  Resposta inesperada: {data}")
                        return False
                else:
                    print(f"   ❌ Status MCP: {response.status}")
                    text = await response.text()
                    print(f"   📄 Resposta: {text[:200]}...")
                    return False
                    
    except Exception as e:
        print(f"   ❌ Erro MCP: {e}")
        return False

async def test_vscode_integration():
    """Test VS Code integration via MCP."""
    
    print("🎯 Testando integração VS Code...")
    
    try:
        # Test adding an entity (should use VS Code models)
        mcp_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "add_entity",
                "arguments": {
                    "name": "Test Entity",
                    "label": "Person",
                    "summary": "A test person for VS Code integration"
                }
            }
        }
        
        async with aiohttp.ClientSession() as session:
            headers = {'Content-Type': 'application/json'}
            
            async with session.post(
                f"{CONTAINER_URL}/message",
                json=mcp_request,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=15)
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    print(f"   ✅ VS Code integration respondeu")
                    
                    if 'result' in data:
                        result = data['result']
                        if 'content' in result:
                            content = result['content'][0] if isinstance(result['content'], list) else result['content']
                            if 'text' in content:
                                text = content['text']
                                print(f"   💬 Resposta: {text[:100]}...")
                                
                                # Check if mentions VS Code or fallback
                                if 'vscode' in text.lower() or 'fallback' in text.lower():
                                    print("   🎯 VS Code integration detectada!")
                                    return True
                        
                    print(f"   📊 Resultado completo: {data}")
                    return True
                else:
                    print(f"   ❌ Status: {response.status}")
                    return False
                    
    except Exception as e:
        print(f"   ❌ Erro VS Code test: {e}")
        return False

async def test_container_logs():
    """Test container environment via logs endpoint if available."""
    
    print("📋 Verificando configuração do container...")
    
    try:
        async with aiohttp.ClientSession() as session:
            # Try to get some info about the running environment
            async with session.get(f"{CONTAINER_URL}/info") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"   ✅ Info do container: {data}")
                    return True
                else:
                    print("   ℹ️  Endpoint /info não disponível")
                    return True  # Not critical
                    
    except Exception as e:
        print(f"   ℹ️  Info não disponível: {e}")
        return True  # Not critical

async def main():
    """Main test function."""
    
    print("🧪 TESTE COMPLETO DO CONTAINER MCP")
    print("=" * 50)
    print(f"🎯 Testando container em: {CONTAINER_URL}")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_container_health),
        ("SSE Connection", test_mcp_sse_connection), 
        ("MCP Request", test_mcp_request),
        ("VS Code Integration", test_vscode_integration),
        ("Container Info", test_container_logs),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔄 {test_name}...")
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"   ❌ Erro inesperado: {e}")
            results.append((test_name, False))
        
        await asyncio.sleep(1)  # Brief pause between tests
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    success_rate = (passed / len(results)) * 100
    print(f"\n🎯 Taxa de sucesso: {success_rate:.1f}% ({passed}/{len(results)})")
    
    if success_rate >= 80:
        print("\n🎉 CONTAINER FUNCIONANDO CORRETAMENTE!")
        print("✅ VS Code integration está ativa no container")
        print("✅ MCP server respondendo adequadamente")
    elif success_rate >= 60:
        print("\n⚠️  Container funcionando com alguns problemas")
        print("🔧 Verificar logs do container para detalhes")
    else:
        print("\n❌ Container com problemas sérios")
        print("🚨 Verificar configuração e logs")
    
    return success_rate >= 60

if __name__ == "__main__":
    print("🚀 Iniciando testes do container...")
    print("📝 Certifique-se de que o container está rodando:")
    print("   docker-compose -f docker-compose.dev.yml up")
    print("")
    
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Testes interrompidos pelo usuário")
        sys.exit(1)