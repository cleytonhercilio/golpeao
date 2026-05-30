#!/bin/bash
set -e

echo "🌐 Iniciando GolPeão Frontend na porta ${PORT:-8501}..."
exec streamlit run "frontend/0_🔐_Login.py" \
  --server.port "${PORT:-8501}" \
  --server.address 0.0.0.0 \
  --server.headless true
