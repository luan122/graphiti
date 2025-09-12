# Script para configurar fork e criar branch feat/vscodemodels
# Execute estes comandos após fazer o fork no GitHub

# 1. Adicionar seu fork como remote (substitua SEU_USERNAME pelo seu username do GitHub)
git remote add fork https://github.com/SEU_USERNAME/graphiti.git

# 2. Verificar remotes configurados
git remote -v

# 3. Criar e mudar para a nova branch
git checkout -b feat/vscodemodels

# 4. Fazer commit das nossas alterações
git add .

# 5. Commit com mensagem descritiva
git commit -m "feat: Add VS Code models integration with MCP server

- Implement VSCodeClient with intelligent fallbacks
- Add VSCodeEmbedder with 1024-dimensional vectors
- Configure Docker environment with live reload
- Add MCP server configurations for multiple transports
- Support multi-provider architecture (OpenAI, Azure, Gemini, VS Code)
- Include comprehensive setup documentation

Features:
- Native VS Code LLM integration
- Semantic embedding consistency
- Docker containerization with Neo4j
- MCP protocol support (SSE and STDIO)
- Development environment setup
- Complete configuration examples"

# 6. Push para o seu fork
git push fork feat/vscodemodels

# 7. (Opcional) Configurar upstream para futuras atualizações
git remote add upstream https://github.com/getzep/graphiti.git