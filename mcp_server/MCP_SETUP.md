# Configuração MCP para Graphiti

Este guia explica como configurar o servidor MCP Graphiti para funcionar com diferentes clientes MCP, incluindo o Claude Desktop.

## Pré-requisitos

1. **Neo4j Database**: Execute o banco Neo4j (pode usar Docker)
2. **Python Environment**: Python 3.10+
3. **Dependencies**: Execute `uv sync` no diretório `mcp_server`

## Configurações Disponíveis

### 1. Configuração Docker (Recomendada para Development)

O servidor está configurado para rodar em Docker com todas as dependências:

```bash
cd mcp_server
docker-compose -f docker-compose.dev.yml up -d
```

**Recursos:**
- ✅ **VS Code Models**: Integração nativa com modelos do VS Code
- ✅ **Embeddings**: VSCodeEmbedder com vetores 1024-dimensional
- ✅ **Neo4j**: Banco de dados em container
- ✅ **Live Reload**: Modificações em tempo real no código

**Acesso:** 
- MCP Server: `http://localhost:8122` (SSE transport)
- Neo4j Browser: `http://localhost:7474` (neo4j/demodemo)

### 2. Claude Desktop Configuration

Para usar com Claude Desktop, adicione ao arquivo de configuração do Claude:

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "graphiti": {
      "command": "uv",
      "args": ["--directory", "CAMINHO_PARA_SEU_REPO\\graphiti\\mcp_server", "run", "python", "graphiti_mcp_server.py"],
      "env": {
        "USE_VSCODE_MODELS": "true",
        "NEO4J_URI": "bolt://localhost:7687", 
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "demodemo",
        "MODEL_NAME": "gpt-4o-mini",
        "SEMAPHORE_LIMIT": "10"
      }
    }
  }
}
```

**⚠️ Importante:** Substitua `CAMINHO_PARA_SEU_REPO` pelo caminho real do seu repositório.

### 3. Configuração Local (Desenvolvimento)

Para executar localmente sem Docker:

```bash
cd mcp_server
# Instalar como pacote editável
pip install -e ..
# Executar servidor
uv run python graphiti_mcp_server.py --transport stdio
```

## Verificação dos Modelos VS Code

Ao iniciar, o servidor deve mostrar logs similares a:

```
INFO - Using vscode LLM - Model: gpt-4o-mini
INFO - Using vscode embedder - Model: embedding-001
INFO - VSCodeEmbedder initialized - VS Code available: True
```

## Recursos Disponíveis

### Ferramentas MCP

- `add_episode`: Adiciona episódios ao grafo de conhecimento
- `search`: Busca semântica no grafo
- `get_nodes`: Recupera nós específicos
- `bulk_episodes`: Adiciona múltiplos episódios
- `delete_episodes`: Remove episódios

### Modelos Suportados

1. **VS Code Models** (Padrão quando USE_VSCODE_MODELS=true)
   - LLM: Modelos nativos do VS Code
   - Embedder: Vetores 1024-dimensional consistentes
   - Fallback: Geração semântica inteligente

2. **Google Gemini** (quando GOOGLE_API_KEY definido)
   - LLM: gemini-2.0-flash, gemini-2.5-flash-lite
   - Embedder: embedding-001

3. **OpenAI** (quando OPENAI_API_KEY definido)
   - LLM: gpt-4o-mini, gpt-4o, gpt-3.5-turbo
   - Embedder: text-embedding-3-small

4. **Azure OpenAI** (quando AZURE_* variáveis definidas)

## Teste do Servidor

Execute o teste para verificar funcionamento:

```bash
cd mcp_server
python simple_test.py
```

## Troubleshooting

### Erro "ModuleNotFoundError: No module named 'graphiti_core'"

**Solução:** Instale o pacote local:
```bash
pip install -e .
```

### VS Code Models não funcionando

**Verificações:**
1. VS Code está aberto?
2. Variável `USE_VSCODE_MODELS=true` está definida?
3. Logs mostram "VS Code available: True"?

### Docker não conecta ao Neo4j

**Verificações:**
1. Containers estão rodando: `docker-compose -f docker-compose.dev.yml ps`
2. Neo4j está healthy
3. Portas 7474 e 7687 não estão em uso

### SSE Transport Issues

Se encontrar problemas com SSE, use STDIO:
```bash
uv run python graphiti_mcp_server.py --transport stdio
```

## Arquivos de Configuração

- `claude_desktop_config.json`: Configuração para Claude Desktop
- `mcp_config_sse.json`: Configuração SSE para outros clientes
- `docker-compose.dev.yml`: Ambiente Docker de desenvolvimento
- `simple_test.py`: Script de teste do servidor

## Status dos Modelos VS Code

✅ **Funcionando no Docker**: Container está usando VS Code models com sucesso
✅ **LLM Integration**: VSCodeClient com fallbacks inteligentes  
✅ **Embedder Integration**: VSCodeEmbedder com vetores consistentes
✅ **Neo4j Database**: Container funcionando corretamente
✅ **MCP Protocol**: Server aceitando requisições via SSE