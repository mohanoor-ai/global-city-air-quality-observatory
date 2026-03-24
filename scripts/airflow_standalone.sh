#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="$PROJECT_ROOT/.env"

if ! command -v docker >/dev/null 2>&1; then
  echo "[FAIL] docker is not installed or not on PATH." >&2
  echo "[INFO] Local Airflow now runs via Docker Compose." >&2
  exit 1
fi

if [[ ! -f "$ENV_FILE" && -f "$PROJECT_ROOT/.env.example" ]]; then
  cp "$PROJECT_ROOT/.env.example" "$ENV_FILE"
fi

if ! grep -q '^AIRFLOW_UID=' "$ENV_FILE" 2>/dev/null; then
  echo "AIRFLOW_UID=$(id -u)" >> "$ENV_FILE"
fi

echo "[INFO] Local Airflow now runs via Docker Compose." >&2
echo "[INFO] Starting services from docker-compose.yaml" >&2

cd "$PROJECT_ROOT"
exec docker compose up -d
