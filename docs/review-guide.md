# Reviewer Guide

This project downloads OpenAQ archive data for five cities, transforms it with
Spark, loads a BigQuery warehouse, builds dbt marts, and shows the result in a
Looker Studio dashboard.

## Where to Look

| Part | File |
|---|---|
| DAG | `airflow/dags/global_city_air_quality_observatory_dag.py` |
| Ingestion | `ingestion/download_air_quality_data.py` |
| City scope | `ingestion/location_targets.csv` |
| Spark transform | `spark/bronze_to_silver.py` |
| Silver quality checks | `spark/check_silver_data_quality.py` |
| Warehouse load | `warehouse/load_to_bigquery.py` |
| dbt project | `dbt/air_quality_project/` |
| Terraform | `terraform/main.tf` |
| Dashboard proof | `docs/execution-evidence.md` |

## What to Expect

Local outputs:
- `data/bronze/location_metadata.csv`
- `data/silver/air_quality_measurements/`
- `data/quality/silver_dq_report.json`

BigQuery tables:
- `air_quality_dw.fct_air_quality_measurements`
- `air_quality_dw.dim_city`
- `air_quality_dw.dim_pollutant`

dbt marts:
- `mart_city_pollution_trends`
- `mart_city_pollutant_distribution`
- `mart_city_extreme_events`
- `mart_city_comparison_summary`
- `mart_pm25_city_daily`

Dashboard proof:
- `docs/images/dashboard_overview.png`
- `docs/images/Global_City_Air_Quality_Observatory_Dashboard.pdf`
