# Script PowerShell para configurar fork e criar branch feat/vscodemodels
# Execute estes comandos após fazer o fork no GitHub

Write-Host "🍴 Configurando fork do repositório Graphiti..." -ForegroundColor Green

# 1. Adicionar seu fork como remote (substitua SEU_USERNAME pelo seu username do GitHub)
Write-Host "📡 Adicionando remote do fork..." -ForegroundColor Yellow
# git remote add fork https://github.com/SEU_USERNAME/graphiti.git

# 2. Verificar remotes configurados
Write-Host "🔍 Verificando remotes..." -ForegroundColor Yellow
git remote -v

# 3. Criar e mudar para a nova branch
Write-Host "🌿 Criando branch feat/vscodemodels..." -ForegroundColor Yellow
git checkout -b feat/vscodemodels

# 4. Verificar status dos arquivos
Write-Host "📋 Status dos arquivos:" -ForegroundColor Yellow
git status --short

# 5. Adicionar todos os arquivos modificados e novos
Write-Host "➕ Adicionando arquivos..." -ForegroundColor Yellow
git add .

# 6. Commit com mensagem descritiva
Write-Host "💾 Fazendo commit..." -ForegroundColor Yellow
git commit -m @"
feat: Add VS Code models integration with MCP server

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
- Complete configuration examples

Files added:
- graphiti_core/llm_client/vscode_client.py
- graphiti_core/embedder/vscode_embedder.py
- mcp_server/docker-compose.dev.yml
- mcp_server/MCP_SETUP.md
- mcp_server/claude_desktop_config.json
- Multiple configuration and test files
"@

Write-Host "✅ Branch feat/vscodemodels criada com sucesso!" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Próximos passos:" -ForegroundColor Cyan
Write-Host "1. Faça o fork em: https://github.com/getzep/graphiti" -ForegroundColor White
Write-Host "2. Substitua SEU_USERNAME no comando de remote" -ForegroundColor White  
Write-Host "3. Execute: git remote add fork https://github.com/SEU_USERNAME/graphiti.git" -ForegroundColor White
Write-Host "4. Execute: git push fork feat/vscodemodels" -ForegroundColor White
Write-Host "5. Crie um Pull Request no GitHub" -ForegroundColor White