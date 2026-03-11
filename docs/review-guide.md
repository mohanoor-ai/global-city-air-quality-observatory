# Review Guide

This is a short reviewer walkthrough.

## 1) Confirm project question and scope

- Open [README.md](/home/moha_/projects/air-quality-data-pipeline/README.md) and check:
  - main question
  - data strategy (`backfill` vs `daily`)
  - current global target list in `ingestion/location_targets.csv`

## 2) Run local pipeline steps

From project root:

```bash
uv run python ingestion/download_air_quality_data.py --mode backfill
uv run python processing/clean_air_quality_data.py
uv run python processing/check_silver_data_quality.py
```

Expected artifacts:

- Silver parquet in `data/silver/`
- DQ report JSON in `data/quality/`

## 3) Warehouse + dbt (if cloud credentials are configured)

```bash
uv run python warehouse/load_to_bigquery.py
cd dbt/air_quality_project
DBT_PROFILES_DIR=$(pwd) CLOUDSDK_CONFIG=/tmp/gcloud GOOGLE_APPLICATION_CREDENTIALS=/tmp/gcloud/application_default_credentials.json ../../.venv-dbt/bin/dbt run
DBT_PROFILES_DIR=$(pwd) CLOUDSDK_CONFIG=/tmp/gcloud GOOGLE_APPLICATION_CREDENTIALS=/tmp/gcloud/application_default_credentials.json ../../.venv-dbt/bin/dbt test
```

## 4) Check marts used by dashboard

- `mart_pm25_by_country`
- `mart_pm25_by_city`
- `mart_pollution_trends`
- `mart_pollutant_distribution`
- `mart_extreme_pollution_events`

## 5) Check limitations

See [submission-notes.md](/home/moha_/projects/air-quality-data-pipeline/docs/submission-notes.md) for what is done, what is partial, and what is planned next.
