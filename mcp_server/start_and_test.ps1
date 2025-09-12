# Script PowerShell para iniciar container e executar testes

Write-Host "🚀 Iniciando Container MCP para Testes" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green

# Verificar se Docker está rodando
try {
    docker info | Out-Null
} catch {
    Write-Host "❌ Docker não está rodando. Inicie o Docker primeiro." -ForegroundColor Red
    exit 1
}

Write-Host "🔧 Construindo e iniciando container..." -ForegroundColor Yellow
docker-compose -f docker-compose.dev.yml up --build -d

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Falha ao construir container" -ForegroundColor Red
    exit 1
}

# Aguardar container inicializar
Write-Host "⏳ Aguardando container inicializar..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

# Verificar se container está rodando
$containerStatus = docker-compose -f docker-compose.dev.yml ps
if ($containerStatus -match "Up") {
    Write-Host "✅ Container está rodando!" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "🧪 Executando testes do container..." -ForegroundColor Cyan
    Write-Host "=====================================" -ForegroundColor Cyan
    
    # Executar testes
    uv run python test_container.py
    
    Write-Host ""
    Write-Host "📋 Status dos containers:" -ForegroundColor Blue
    docker-compose -f docker-compose.dev.yml ps
    
}
else {
    Write-Host "❌ Container falhou ao iniciar" -ForegroundColor Red
    Write-Host "📋 Verificando logs..." -ForegroundColor Yellow
    docker-compose -f docker-compose.dev.yml logs
    exit 1
}

Write-Host ""
Write-Host "ℹ️  Para parar o container:" -ForegroundColor Blue
Write-Host "   docker-compose -f docker-compose.dev.yml down" -ForegroundColor Gray