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
gcloud auth login
gcloud auth application-default login
bash scripts/dbt_run.sh
bash scripts/dbt_test.sh
```

## 4) Check marts used by dashboard

- `mart_pm25_by_country`
- `mart_pm25_by_city`
- `mart_pollution_trends`
- `mart_pollutant_distribution`
- `mart_extreme_pollution_events`

## 5) Check final scope

See [submission-notes.md](/home/moha_/projects/air-quality-data-pipeline/docs/submission-notes.md) for the final delivered scope.
