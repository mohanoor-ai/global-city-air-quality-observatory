#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

export AIRFLOW_HOME="${AIRFLOW_HOME:-$PROJECT_ROOT/.airflow}"
export AIRFLOW__CORE__DAGS_FOLDER="${AIRFLOW__CORE__DAGS_FOLDER:-$PROJECT_ROOT/airflow}"
export AIRFLOW__CORE__LOAD_EXAMPLES="${AIRFLOW__CORE__LOAD_EXAMPLES:-False}"

if ! command -v airflow >/dev/null 2>&1; then
  echo "[FAIL] airflow is not installed in the active environment." >&2
  echo "[INFO] Create a dedicated Airflow environment, then rerun this script:" >&2
  echo "  uv venv .venv-airflow --python 3.11" >&2
  echo "  source .venv-airflow/bin/activate" >&2
  echo "  uv pip install apache-airflow" >&2
  exit 1
fi

exec airflow standalone
