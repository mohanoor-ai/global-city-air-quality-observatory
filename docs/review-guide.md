# Reviewer Guide

This project downloads OpenAQ archive data for five cities, transforms it with
Spark, loads a BigQuery warehouse, builds dbt marts, and shows the result in a
Looker Studio dashboard.

Latest committed run evidence in this repo is from March 14, 2026.

## Quick Review Path

1. Read `README.md` for the project scope, architecture, and outputs.
2. Open `docs/execution-evidence.md` for the committed run artifacts and verification notes.
3. Review `docs/images/dashboard_overview.png` and `docs/images/Global_City_Air_Quality_Observatory_Dashboard.pdf`.
4. Run `make test` for local unit checks that do not require cloud credentials.

## Reviewer Prerequisites

- For document-only review, no cloud access is required.
- For local unit tests, install Python dependencies from `requirements.txt`.
- For a full end-to-end rerun, you need `gcloud`, Terraform, Docker Compose, and access to the configured GCP project resources.
- For local Airflow, copy `.env.example` to `.env` and set `GCP_PROJECT_ID`, `GCS_BUCKET_NAME`, and `GOOGLE_APPLICATION_CREDENTIALS`.

## Where to Look

| Part | File |
|---|---|
| DAG | `airflow/dags/global_city_air_quality_observatory_dag.py` |
| Ingestion | `ingestion/download_air_quality_data.py` |
| City scope | `ingestion/location_targets.csv` |
| Spark transform | `spark/bronze_to_silver.py` |
| Silver quality checks | `spark/check_silver_data_quality.py` |
| Warehouse load | `warehouse/load_to_bigquery.py` |
| dbt project | `dbt/air_quality_project/` |
| Terraform | `terraform/main.tf` |
| Dashboard proof | `docs/execution-evidence.md` |

## What to Expect

Local outputs:
- `data/bronze/location_metadata.csv`
- `data/silver/air_quality_measurements/`
- `data/quality/silver_dq_report.json`

BigQuery tables:
- `air_quality_dw.fct_air_quality_measurements`
- `air_quality_dw.dim_city`
- `air_quality_dw.dim_pollutant`

dbt marts:
- `mart_city_pollution_trends`
- `mart_city_pollutant_distribution`
- `mart_city_extreme_events`
- `mart_city_comparison_summary`
- `mart_pm25_city_daily`

Dashboard proof:
- `docs/images/dashboard_overview.png`
- `docs/images/Global_City_Air_Quality_Observatory_Dashboard.pdf`
