# Pipeline Overview

This project uses a batch ELT flow centered on PM2.5 analysis.

## Data flow

```text
OpenAQ archive (csv.gz)
  -> ingestion (backfill or daily)
  -> Bronze files in data/bronze/
  -> Silver cleaning in processing/clean_air_quality_data.py
  -> Silver DQ checks in processing/check_silver_data_quality.py
  -> BigQuery load in warehouse/load_to_bigquery.py
  -> dbt staging + marts
  -> dashboard queries
```

## Ingestion modes

- Backfill: last 2 full years + current year-to-date
- Daily: newest available file per location target

## Location coverage

Location scope is controlled by `ingestion/location_targets.csv`.  
Country and city values in Silver come from this target file metadata.

## Main outputs

- Curated warehouse table: `air_quality_measurements`
- Marts:
  - `mart_pm25_by_country`
  - `mart_pm25_by_city`
  - `mart_pollution_trends`
  - `mart_pollutant_distribution`
  - `mart_extreme_pollution_events`
