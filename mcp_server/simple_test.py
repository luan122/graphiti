#!/usr/bin/env python3
"""
Teste simples para verificar se os modelos VS Code estão funcionando no container Docker
"""

import requests
import json
import time

def test_mcp_server():
    print("🚀 Testando MCP Server no Docker...")
    
    # 1. Obter session_id
    print("\n📡 Obtendo session_id...")
    try:
        response = requests.get("http://localhost:8122/sse", stream=True, timeout=5)
        lines = []
        for line in response.iter_lines():
            if line:
                lines.append(line.decode('utf-8'))
                if len(lines) >= 2:  # event e data
                    break
        
        session_id = None
        for line in lines:
            if line.startswith('data: /messages/?session_id='):
                session_id = line.split('session_id=')[1]
                break
        
        if session_id:
            print(f"✅ Session ID obtido: {session_id}")
        else:
            print("❌ Não foi possível obter session_id")
            return
            
    except Exception as e:
        print(f"❌ Erro ao obter session_id: {e}")
        return
    
    # 2. Testar lista de ferramentas
    print(f"\n🛠️  Testando lista de ferramentas...")
    try:
        url = f"http://localhost:8122/messages/?session_id={session_id}"
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list"
        }
        
        response = requests.post(url, json=payload, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"❌ Erro ao testar ferramentas: {e}")
    
    # 3. Testar add_episode (teste LLM)
    print(f"\n📝 Testando add_episode (VS Code LLM)...")
    try:
        url = f"http://localhost:8122/messages/?session_id={session_id}"
        payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "add_episode",
                "arguments": {
                    "name": "Teste VS Code Models Docker",
                    "content": "Este é um teste para verificar se os modelos VS Code estão funcionando corretamente no container Docker. Testando LLM e embedder."
                }
            }
        }
        
        response = requests.post(url, json=payload, timeout=30)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"❌ Erro ao testar add_episode: {e}")

if __name__ == "__main__":
    test_mcp_server()