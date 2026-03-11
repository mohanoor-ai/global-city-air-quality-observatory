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
cd dbt/air_quality_project
DBT_PROFILES_DIR=$(pwd) CLOUDSDK_CONFIG=/tmp/gcloud GOOGLE_APPLICATION_CREDENTIALS=/tmp/gcloud/application_default_credentials.json ../../.venv-dbt/bin/dbt run
DBT_PROFILES_DIR=$(pwd) CLOUDSDK_CONFIG=/tmp/gcloud GOOGLE_APPLICATION_CREDENTIALS=/tmp/gcloud/application_default_credentials.json ../../.venv-dbt/bin/dbt test
```
