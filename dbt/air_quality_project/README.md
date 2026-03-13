# dbt Project

This dbt project builds dashboard-ready marts from `fct_air_quality_measurements`.

Models:

- staging: `stg_air_quality`
- marts: `mart_city_pollution_trends`, `mart_city_pollutant_distribution`, `mart_city_extreme_events`, `mart_city_comparison_summary`, `mart_pm25_city_daily`

Run:

```bash
gcloud auth login
gcloud auth application-default login
bash scripts/dbt_run.sh
bash scripts/dbt_test.sh
```
