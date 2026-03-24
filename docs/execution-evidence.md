# Execution Evidence

Latest committed run evidence in this repo is from March 14, 2026.

## Local Outputs

- `data/bronze/location_metadata.csv`
- `data/silver/air_quality_measurements/`
- `data/silver/latest_run_summary.json`
- `data/quality/silver_dq_report.json`

## BigQuery Tables

- `air_quality_dw.fct_air_quality_measurements`
- `air_quality_dw.dim_city`
- `air_quality_dw.dim_pollutant`

## dbt Marts

- `mart_city_pollution_trends`
- `mart_city_pollutant_distribution`
- `mart_city_extreme_events`
- `mart_city_comparison_summary`
- `mart_pm25_city_daily`

## Committed Proof Files

- `images/airflow_dag_graph.png`
- `images/airflow_success_run.png`
- `images/bronze_ingestion_success.png`
- `images/silver_quality_report.png`
- `images/load_to_bigquery.png`
- `images/bigquery_tables.png`
- `images/dbt_run_output.png`
- `images/dbt_test_output.png`
- `images/gcs_silver_staging.png`
- `images/dashboard_overview.png`
- `images/Global_City_Air_Quality_Observatory_Dashboard.pdf`

## Verification Notes

- The GCS staging screenshot was captured from `gcloud storage ls --long gs://aq-lake-moha/silver/air_quality_measurements/`.
- The saved Silver quality report shows `status: pass`, `row_count: 185473`, and the five expected cities.
- The committed dbt test screenshot shows `PASS=25 WARN=0 ERROR=0`.

## Dashboard Proof

![Dashboard overview](images/dashboard_overview.png)

- Live dashboard: [Global City Air Quality Observatory Looker Studio dashboard](https://lookerstudio.google.com/reporting/6432e2e1-4363-493c-bbf8-598c60bb49de)
- PDF export: [Global City Air Quality Observatory dashboard PDF](images/Global_City_Air_Quality_Observatory_Dashboard.pdf)
