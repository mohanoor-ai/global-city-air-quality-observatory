# Air Quality Data Pipeline

End-to-end batch pipeline for PM2.5-focused country and city analysis using OpenAQ historical archive data.

## Project Overview

Air pollution data is large and fragmented across many monitoring stations.  
This project builds a clear data flow from raw OpenAQ files to analytics marts used for reporting.

The pipeline:

- ingests archive files from OpenAQ (AWS Open Data)
- stores raw files in a Bronze layer
- cleans and standardizes data into a Silver layer
- runs data quality checks before warehouse load
- loads curated data to BigQuery
- builds analytics marts with dbt

## Main Question

Which countries and cities have the worst PM2.5 exposure over time, and where are trends improving or worsening?

## Data Strategy

- `backfill` mode: last 2 full years + current year-to-date
- `daily` mode: newest available file per configured location

Location scope is controlled by `ingestion/location_targets.csv`.

Current global starter targets (one city per inhabited continent):

- Cairo, EG
- Delhi, IN
- London, GB
- Mexico City, MX
- Buenos Aires, AR
- Sydney, AU

## Dashboard Story

1. Global trend: how pollution changes over time
2. Worst countries: highest average PM2.5
3. Worst cities: highest average PM2.5
4. Pollutant comparison: how major pollutants differ across locations

## Core Metrics

- average PM2.5 by country
- average PM2.5 by city
- monthly pollution trend over time
- highest recorded pollutant value by location
- pollutant distribution by type

## Architecture

```text
OpenAQ AWS Archive (csv.gz)
        ↓
Python Ingestion (backfill / daily)
        ↓
Bronze Layer (raw csv.gz files)
        ↓
Silver Layer (cleaned parquet)
        ↓
Data Quality Gate
        ↓
BigQuery Warehouse Table
        ↓
dbt Staging + Marts
        ↓
Dashboard
```

Airflow orchestration includes two DAG entrypoints:

- `air_quality_backfill_pipeline_dag` (manual)
- `air_quality_daily_pipeline_dag` (`@daily`)

## Final Mart Tables

- `mart_pm25_by_country`
- `mart_pm25_by_city`
- `mart_pollution_trends`
- `mart_pollutant_distribution`
- `mart_extreme_pollution_events`

## Technology Stack

- ingestion: Python (`boto3`)
- processing: Pandas
- data quality: Python checks + JSON report
- warehouse: BigQuery
- transformation: dbt
- orchestration: Airflow
- infrastructure: Terraform (minimal scaffold)
- dashboard: Looker Studio
- environment: `uv`

## Quick Start

```bash
uv sync
uv run python ingestion/download_air_quality_data.py --mode backfill
uv run python processing/clean_air_quality_data.py
uv run python processing/check_silver_data_quality.py
```

Quick city-vs-city comparison (PM2.5 by default):

```bash
uv run python scripts/compare_city_pollution.py --city-a "Delhi" --city-b "London"
```

Optional cloud steps:

```bash
uv run python warehouse/load_to_bigquery.py
gcloud auth login
gcloud auth application-default login
bash scripts/dbt_run.sh
bash scripts/dbt_test.sh
```

## Implemented Now

- ingestion with `backfill` and `daily` modes
- Silver cleaning with pollutant normalization and location enrichment
- Silver data quality gate
- BigQuery load script for curated warehouse table
- dbt staging and final marts
- Airflow DAG entrypoints for backfill and daily runs
- lightweight unit tests

## Limitations

- country and city coverage depends on configured target locations
- comparative rankings are only as broad as current location coverage
- dashboard screenshot evidence is tracked in `images/` and may be incomplete until final capture

## Documentation

- Overview: `docs/pipeline-overview.md`
- Data source: `docs/data-source.md`
- Architecture decisions: `docs/architecture-decisions.md`
- Run commands and validation SQL: `runbook.md`
- Dashboard mapping: `dashboards/README.md`
- Custom city/location testing: `docs/custom-location-testing.md`
- Infrastructure scope: `docs/infrastructure.md`
- Review walkthrough: `docs/review-guide.md`
- Final scope summary: `docs/submission-notes.md`
