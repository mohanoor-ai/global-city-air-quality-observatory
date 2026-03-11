# Project Plan

This file tracks real status only.

## Implemented now

- OpenAQ archive ingestion with two modes:
  - `backfill` (last 2 full years + current YTD)
  - `daily` (latest file per configured location)
- Global starter target list (one major city per inhabited continent)
- Bronze to Silver processing with pollutant normalization
- Silver data quality check script with JSON report output
- Warehouse load script (latest Silver parquet -> GCS -> BigQuery)
- dbt staging model plus five marts:
  - `mart_pm25_by_country`
  - `mart_pm25_by_city`
  - `mart_pollution_trends`
  - `mart_pollutant_distribution`
  - `mart_extreme_pollution_events`
- Simple Airflow DAG entrypoints for backfill and daily runs
- Lightweight unit tests for ingestion/date-window logic and Silver checks

## Partially implemented

- Terraform is a minimal scaffold for bucket + dataset + one warehouse table.
- Dashboard design and mart mapping docs are ready, but screenshots and final published dashboard evidence are not complete in the repo.

## Planned next

- Run one fresh end-to-end cloud execution with the updated 6-city global targets and record validation output in the runbook.
- Add mart-level validation query results (row counts and grain checks) after dbt run/test.
- Save dashboard screenshots in `images/` and link them in `dashboards/README.md`.
