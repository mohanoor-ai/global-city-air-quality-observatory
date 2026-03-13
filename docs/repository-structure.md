# Repository Structure

This document explains how the repository is organized.

The goal is to keep the project easy to understand, maintain, and reproduce.

---

## Root Structure

```text
air-quality-data-pipeline/
├── README.md
├── airflow/
├── dashboards/
├── data/
├── dbt/
├── docs/
├── ingestion/
├── spark/
├── scripts/
├── sql/
├── terraform/
└── tests/
```

## Key Pipeline Files

```text
ingestion/
  download_air_quality_data.py

spark/
  bronze_to_silver.py
  check_silver_data_quality.py   # Data quality checks (quality gate)

sql/
  warehouse_validation.sql       # Warehouse-level validation queries
  mart_validation.sql            # Mart-level row count + grain checks

scripts/
  dbt_run.sh                     # wrapper for dbt run
  dbt_test.sh                    # wrapper for dbt test
  compare_city_pollution.py      # quick city-vs-city pollution comparison
```
