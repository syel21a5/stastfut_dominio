#!/bin/bash
set -e

echo "==============================================="
echo "   INICIANDO CORREÇÃO TOTAL DO DEPLOY"
echo "==============================================="

# 1. Garantir que estamos na raiz do projeto
cd "$(dirname "$0")"

# 2. Forçar atualização do código (sobrescreve tudo local)
echo "⬇️  Baixando código mais recente do GitHub..."
git fetch --all
git reset --hard origin/main
git pull origin main

# 3. Recriar o arquivo .env do zero
# Isso elimina qualquer erro de digitação ou formatação anterior
echo "📝 Recriando arquivo de configuração (.env)..."
cat > .env <<EOF
DEBUG=False
SECRET_KEY=django-insecure-fix-$(date +%s)
ALLOWED_HOSTS=teste1.statsfut.com,www.teste1.statsfut.com,localhost,127.0.0.1,104.248.229.208
CSRF_TRUSTED_ORIGINS=https://teste1.statsfut.com,http://teste1.statsfut.com,http://localhost:8081
DB_NAME=betstats
DB_USER=root
DB_PASSWORD=root
DB_HOST=db
DB_PORT=3306
EOF

# 4. Ajustar permissões
echo "🔧 Ajustando permissões..."
chmod +x entrypoint.sh

# 5. Reiniciar Containers (Forçando recriação)
echo "♻️  Reiniciando Docker..."
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d --build --force-recreate

echo "==============================================="
echo "   ✅ CORREÇÃO CONCLUÍDA!"
echo "   Aguarde 10 segundos e recarregue a página."
echo "==============================================="
