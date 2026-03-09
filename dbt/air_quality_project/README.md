# dbt Project

This dbt project transforms warehouse air quality data into analytics models.

## Included Models

- `stg_air_quality` (staging view)
- `mart_pollution_by_city` (city-level mart table)

## Setup

1. Copy profile template:

```bash
cp dbt/air_quality_project/profiles.yml.example ~/.dbt/profiles.yml
```

2. Run dbt from project directory:

```bash
cd dbt/air_quality_project
dbt debug
dbt run
dbt test
```
