# Pipeline Runbook

This runbook contains the practical command sequence to run the pipeline.

---

## Prerequisites

- `uv sync` completed
- Terraform infrastructure already applied
- GCP authentication completed:
  - `gcloud auth login`
  - `gcloud auth application-default login`

---

## End-to-End Batch Run (Manual)

From project root:

```bash
# 1) Optional source inspection (quick key listing by location/year/month)
# Use ingestion script logs during backfill to confirm keys are being discovered.
uv run python ingestion/download_air_quality_data.py --mode backfill
uv run python processing/clean_air_quality_data.py
uv run python processing/check_silver_data_quality.py
uv run python warehouse/load_to_bigquery.py
```

Optional quick comparison:

```bash
uv run python scripts/compare_city_pollution.py --city-a "Delhi" --city-b "London"
```

Daily refresh only:

```bash
uv run python ingestion/download_air_quality_data.py --mode daily
uv run python processing/clean_air_quality_data.py
uv run python processing/check_silver_data_quality.py
uv run python warehouse/load_to_bigquery.py
```

---

## dbt Models

Use the wrapper scripts:

```bash
gcloud auth login
gcloud auth application-default login
bash scripts/dbt_run.sh
bash scripts/dbt_test.sh
```

---

## Automated Run (Airflow DAG)

DAG file:

`airflow/air_quality_pipeline_dag.py`

Task flow:

`ingest_bronze -> build_silver -> data_quality_gate -> load_warehouse -> dbt_run -> dbt_test`

DAGs:

- `air_quality_backfill_pipeline_dag` (manual trigger)
- `air_quality_daily_pipeline_dag` (`@daily` schedule)

---

## Quick Validation Queries (BigQuery)

```sql
SELECT COUNT(*) FROM `aq-pipeline-260309-5800.air_quality_dw.air_quality_measurements`;
SELECT COUNT(*) FROM `aq-pipeline-260309-5800.air_quality_dbt_marts.mart_pm25_by_city`;
SELECT COUNT(*) FROM `aq-pipeline-260309-5800.air_quality_dbt_marts.mart_pm25_by_country`;
SELECT COUNT(*) FROM `aq-pipeline-260309-5800.air_quality_dbt_marts.mart_pollution_trends`;
SELECT COUNT(*) FROM `aq-pipeline-260309-5800.air_quality_dbt_marts.mart_pollutant_distribution`;
SELECT COUNT(*) FROM `aq-pipeline-260309-5800.air_quality_dbt_marts.mart_extreme_pollution_events`;
```

## Mart Grain Checks (BigQuery)

Use these after `dbt run`:

```sql
-- mart_pm25_by_country grain: month_start, country
SELECT month_start, country, COUNT(*) AS row_count
FROM `aq-pipeline-260309-5800.air_quality_dbt_marts.mart_pm25_by_country`
GROUP BY month_start, country
HAVING COUNT(*) > 1;

-- mart_pm25_by_city grain: month_start, country, city
SELECT month_start, country, city, COUNT(*) AS row_count
FROM `aq-pipeline-260309-5800.air_quality_dbt_marts.mart_pm25_by_city`
GROUP BY month_start, country, city
HAVING COUNT(*) > 1;
```

Saved query files:

- `sql/warehouse_validation.sql`
- `sql/mart_validation.sql`
