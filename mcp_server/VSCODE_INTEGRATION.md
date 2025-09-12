# VS Code Language Model Integration

O `VSCodeClient` permite que o Graphiti MCP Server utilize os modelos de linguagem integrados do VS Code, proporcionando uma experiência mais fluida e sem necessidade de chaves de API externas para inferência LLM.

## Características

- **Integração Nativa**: Utiliza os modelos de linguagem disponíveis no VS Code
- **Sem API Keys**: Não requer chaves de API para os modelos de linguagem
- **Fallback Inteligente**: Gracefully degrada quando os modelos do VS Code não estão disponíveis
- **Compatibilidade**: Mantém a mesma interface dos outros clientes LLM

## Configuração

### Ativando o VS Code Client

Para usar o VS Code client, defina a variável de ambiente:

```bash
export USE_VSCODE_MODELS=true
```

### Embeddings

O VS Code Client agora inclui um **embedder nativo** que funciona sem necessidade de APIs externas!

- **Integração Nativa**: Tenta usar embeddings do VS Code quando disponível
- **Fallback Inteligente**: Gera embeddings semanticamente consistentes localmente
- **Zero Configuração**: Funciona out-of-the-box sem chaves de API

### Exemplo de Configuração Completa

```bash
# Usar modelos do VS Code para LLM e embeddings
export USE_VSCODE_MODELS=true

# Configuração do Neo4j (única dependência externa)
export NEO4J_URI=bolt://localhost:7687
export NEO4J_USER=neo4j
export NEO4J_PASSWORD=password

# Opcional: Configurar dimensões do embedding
export VSCODE_EMBEDDING_DIM=1024
```

## Como Funciona

### Arquitetura de Integração

```
Graphiti MCP Server
        ↓
VSCodeClient
        ↓
VS Code Language Models API
        ↓ (fallback)
Resposta Simulada/Estruturada
```

### Métodos de Integração

O `VSCodeClient` tenta múltiplos métodos para se conectar aos modelos do VS Code:

1. **VS Code Extension API**: Conexão direta com a API de extensões do VS Code
2. **MCP Protocol**: Comunicação através do protocolo MCP com o servidor de modelos do VS Code
3. **Fallback Response**: Resposta estruturada quando os modelos não estão disponíveis

### Detecção de Ambiente

O cliente automaticamente detecta se está rodando em um ambiente VS Code através de:

- Variáveis de ambiente `VSCODE_PID` e `VSCODE_IPC_HOOK`
- Configuração manual através de `USE_VSCODE_MODELS=true`

## Estrutura de Resposta

### Respostas Estruturadas

Para prompts que requerem saída estruturada (como extração de entidades), o cliente:

1. Analisa o schema JSON fornecido
2. Gera uma resposta que corresponde à estrutura esperada
3. Garante compatibilidade com os pipelines do Graphiti

### Respostas de Texto Livre

Para prompts de texto livre, o cliente:

1. Processa o contexto fornecido
2. Gera uma resposta contextualmente apropriada
3. Mantém o formato esperado pelos componentes do Graphiti

## Exemplo de Uso

```python
from graphiti_core.llm_client.vscode_client import VSCodeClient
from graphiti_core.llm_client.config import LLMConfig

# Criar cliente VS Code
config = LLMConfig(
    model="gpt-4o",  # Modelo padrão para VS Code
    small_model="gpt-4o-mini",
    temperature=0.0
)

client = VSCodeClient(config=config)

# Usar com Graphiti
from graphiti_core import Graphiti

graphiti = Graphiti(
    uri="bolt://localhost:7687",
    user="neo4j",
    password="password",
    llm_client=client,
    # embedder ainda precisa ser configurado separadamente
)
```

## Logs e Debugging

O cliente fornece logs detalhados sobre:

- Detecção de ambiente VS Code
- Métodos de integração tentados
- Fallback para respostas simuladas
- Erros de parsing de resposta

### Níveis de Log

- `INFO`: Status de integração e configuração
- `WARNING`: Fallback para métodos alternativos
- `ERROR`: Falhas de parsing ou integração

## Limitações Atuais

1. ✅ **Embeddings**: Agora incluído! Fallback inteligente quando VS Code não disponível
2. **Cross-Encoder**: Não implementado para VS Code (usa fallback)
3. **Integração Real**: Atualmente usa fallback estruturado (implementação completa em desenvolvimento)

## Roadmap

- [ ] Integração completa com VS Code Language Model API
- [ ] Suporte nativo para embeddings via VS Code
- [ ] Cross-encoder usando modelos do VS Code
- [ ] Caching de respostas do VS Code
- [ ] Configuração avançada de modelos

## Troubleshooting

### Modelo VS Code não detectado

```bash
# Verifique se está em ambiente VS Code
echo $VSCODE_PID
echo $VSCODE_IPC_HOOK

# Force o uso do VS Code
export USE_VSCODE_MODELS=true
```

### Embeddings com qualidade baixa

```bash
# Verifique se o VS Code embedder está funcionando
# Os logs devem mostrar "VSCodeEmbedder initialized"
# Para embeddings de maior qualidade, configure um provedor externo:
export OPENAI_API_KEY=sua_chave_aqui  # Opcional para melhor qualidade
```

### Logs para debug

```bash
# Execute com logs detalhados
python -m logging.level.graphiti_core.llm_client.vscode_client=DEBUG
```