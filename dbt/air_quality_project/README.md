# dbt Project

This dbt project builds PM2.5-focused marts from `air_quality_measurements`.

## Models

Staging:

- `stg_air_quality`

Marts:

- `mart_pm25_by_country`
- `mart_pm25_by_city`
- `mart_pollution_trends`
- `mart_pollutant_distribution`
- `mart_extreme_pollution_events`

## Run

```bash
gcloud auth login
gcloud auth application-default login
bash scripts/dbt_run.sh
bash scripts/dbt_test.sh
```
