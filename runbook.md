# Pipeline Runbook

This runbook contains the practical command sequence to run the pipeline.

---

## Prerequisites

- `uv sync` completed
- Terraform infrastructure already applied
- GCP auth configured (`CLOUDSDK_CONFIG=/tmp/gcloud` in this project setup)

---

## End-to-End Batch Run (Manual)

From project root:

```bash
uv run python ingestion/download_air_quality_data.py
uv run python processing/clean_air_quality_data.py
uv run python processing/check_silver_data_quality.py
uv run python warehouse/load_to_bigquery.py
```

---

## dbt Models

Use the dbt Python 3.12 environment:

```bash
cd dbt/air_quality_project
DBT_PROFILES_DIR=$(pwd) CLOUDSDK_CONFIG=/tmp/gcloud GOOGLE_APPLICATION_CREDENTIALS=/tmp/gcloud/application_default_credentials.json ../../.venv-dbt/bin/dbt run
DBT_PROFILES_DIR=$(pwd) CLOUDSDK_CONFIG=/tmp/gcloud GOOGLE_APPLICATION_CREDENTIALS=/tmp/gcloud/application_default_credentials.json ../../.venv-dbt/bin/dbt test
```

---

## Automated Run (Airflow DAG)

DAG file:

`airflow/air_quality_pipeline_dag.py`

Task flow:

`build_silver -> data_quality_gate -> load_warehouse -> dbt_run -> dbt_test`

---

## Quick Validation Queries (BigQuery)

```sql
SELECT COUNT(*) FROM `aq-pipeline-260309-5800.air_quality_dw.air_quality_measurements`;
SELECT COUNT(*) FROM `aq-pipeline-260309-5800.air_quality_dbt_marts.mart_pollution_by_city`;
SELECT COUNT(*) FROM `aq-pipeline-260309-5800.air_quality_dbt_marts.mart_pollution_by_country`;
SELECT COUNT(*) FROM `aq-pipeline-260309-5800.air_quality_dbt_marts.mart_pollution_trends`;
```
