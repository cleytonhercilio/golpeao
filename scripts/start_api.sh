#!/bin/bash
set -e

echo "🚀 Iniciando GolPeão API..."
echo "📦 Populando banco de dados (times, jogos, achievements)..."
python scripts/seed_db.py

echo "⚡ Iniciando servidor FastAPI na porta ${PORT:-8000}..."
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
