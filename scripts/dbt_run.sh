#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DBT_PROJECT_DIR="$PROJECT_ROOT/dbt/air_quality_project"

export DBT_PROFILES_DIR="$DBT_PROJECT_DIR"

"$PROJECT_ROOT/.venv-dbt/bin/dbt" run --project-dir "$DBT_PROJECT_DIR"
