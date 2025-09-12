#!/usr/bin/env bash
# Script para iniciar o container e executar testes

echo "🚀 Iniciando Container MCP para Testes"
echo "======================================"

# Verificar se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker não está rodando. Inicie o Docker primeiro."
    exit 1
fi

echo "🔧 Construindo e iniciando container..."
docker-compose -f docker-compose.dev.yml up --build -d

# Aguardar container inicializar
echo "⏳ Aguardando container inicializar..."
sleep 10

# Verificar se container está rodando
if docker-compose -f docker-compose.dev.yml ps | grep -q "Up"; then
    echo "✅ Container está rodando!"
    
    echo ""
    echo "🧪 Executando testes do container..."
    echo "====================================="
    
    # Executar testes
    uv run python test_container.py
    
    echo ""
    echo "📋 Status dos containers:"
    docker-compose -f docker-compose.dev.yml ps
    
else
    echo "❌ Container falhou ao iniciar"
    echo "📋 Verificando logs..."
    docker-compose -f docker-compose.dev.yml logs
    exit 1
fi

echo ""
echo "ℹ️  Para parar o container:"
echo "   docker-compose -f docker-compose.dev.yml down"