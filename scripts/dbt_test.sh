#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DBT_PROJECT_DIR="$PROJECT_ROOT/dbt/air_quality_project"
TFVARS_FILE="$PROJECT_ROOT/terraform/terraform.tfvars"

tfvars_value() {
  local key="$1"
  sed -n "s/^${key}[[:space:]]*=[[:space:]]*\"\\(.*\\)\"/\\1/p" "$TFVARS_FILE" | head -n 1
}

export DBT_PROFILES_DIR="$DBT_PROJECT_DIR"
export PROJECT_ID="${PROJECT_ID:-$(tfvars_value project_id)}"
export BIGQUERY_LOCATION="${BIGQUERY_LOCATION:-$(tfvars_value bigquery_location)}"
export DBT_DATASET="${DBT_DATASET:-air_quality_dbt}"

if [[ -z "${CLOUDSDK_CONFIG:-}" && -d /tmp/gcloud ]]; then
  export CLOUDSDK_CONFIG=/tmp/gcloud
fi

DEFAULT_ADC_FILE="$HOME/.config/gcloud/application_default_credentials.json"
CONFIG_ADC_FILE="${CLOUDSDK_CONFIG:-}/application_default_credentials.json"
ADC_FILE="${GOOGLE_APPLICATION_CREDENTIALS:-}"
if [[ -z "$ADC_FILE" ]]; then
  if [[ -f "$DEFAULT_ADC_FILE" ]]; then
    ADC_FILE="$DEFAULT_ADC_FILE"
  elif [[ -n "${CLOUDSDK_CONFIG:-}" && -f "$CONFIG_ADC_FILE" ]]; then
    ADC_FILE="$CONFIG_ADC_FILE"
  else
    ADC_FILE="$DEFAULT_ADC_FILE"
  fi
fi
if [[ ! -f "$ADC_FILE" ]]; then
  echo "[FAIL] Missing Application Default Credentials: $ADC_FILE" >&2
  echo "[INFO] Run: gcloud auth application-default login --no-launch-browser" >&2
  exit 1
fi
export GOOGLE_APPLICATION_CREDENTIALS="$ADC_FILE"

"$PROJECT_ROOT/.venv-dbt/bin/python" -c "from dbt.cli.main import cli; raise SystemExit(cli())" \
  test --project-dir "$DBT_PROJECT_DIR"
