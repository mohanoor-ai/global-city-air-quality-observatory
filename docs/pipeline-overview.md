# Pipeline Overview

This project uses a batch ELT flow centered on five-city comparison analytics.

## Data flow

```text
OpenAQ archive (csv.gz)
  -> Python ingestion (backfill or daily)
  -> Bronze files in data/bronze/
  -> Spark Silver transform in spark/bronze_to_silver.py
  -> Silver DQ checks in spark/check_silver_data_quality.py
  -> BigQuery load in warehouse/load_to_bigquery.py
  -> dbt staging + marts
  -> Looker Studio dashboard
```

## Ingestion modes

- Backfill: last 2 full years + current year-to-date
- Daily: newest available file per configured city

## Main outputs

- Warehouse fact: `fct_air_quality_measurements`
- Dimensions: `dim_city`, `dim_pollutant`
- Marts: `mart_city_pollution_trends`, `mart_city_pollutant_distribution`, `mart_city_extreme_events`, `mart_city_comparison_summary`, `mart_pm25_city_daily`
