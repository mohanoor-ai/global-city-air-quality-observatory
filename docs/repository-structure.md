# Repository Structure

This document explains how the repository is organized.

The goal is to keep the project easy to understand, maintain, and reproduce.

---

## Root Structure

```text
global-city-air-quality-observatory/
├── README.md
├── airflow/
├── dashboards/
├── dbt/
├── docs/
├── ingestion/
├── legacy_processing/
├── main.py
├── runbook.md
├── spark/
├── terraform/
├── tests/
└── warehouse/
```

Supporting helper folders also exist for dbt shell wrappers, SQL validation queries, architecture images, and legacy files, but they are not presented as the main transformation path.

## Key Pipeline Files

```text
ingestion/
  download_air_quality_data.py
  location_targets.csv
  city_scope.py

spark/
  bronze_to_silver.py            # Bronze to Silver Spark transformation
  check_silver_data_quality.py   # Silver quality gate

warehouse/
  load_to_bigquery.py            # Partitioned and clustered BigQuery load

airflow/
  global_city_air_quality_observatory_dag.py    # Backfill and daily orchestration DAGs

dbt/air_quality_project/models/marts/reporting/
  mart_pm25_city_daily.sql
  mart_city_pollution_trends.sql
  mart_city_pollutant_distribution.sql
  mart_city_extreme_events.sql
  mart_city_comparison_summary.sql

scripts/
  dbt_run.sh                     # wrapper for dbt run
  dbt_test.sh                    # wrapper for dbt test
  compare_city_pollution.py      # quick city-vs-city pollution comparison
```
