# Project Plan

This project is finalized.

## Completed Scope

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
