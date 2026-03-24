# Execution evidence

This document provides proof that the Global City Air Quality Observatory pipeline ran successfully across orchestration, transformation, warehouse loading, and visualization layers.

All proof-of-run assets referenced below are committed in `docs/images/`.

Committed evidence files used in this document:

- `airflow_dag_graph.png`
- `airflow_success_run.png`
- `bronze_ingestion_success.png`
- `silver_quality_report.png`
- `dbt_run_output.png`
- `dbt_test_output.png`
- `load_to_bigquery.png`
- `bigquery_tables.png`
- `dashboard_overview.png`
- `Global_City_Air_Quality_Observatory_Dashboard.pdf`

## Airflow

### DAG structure
![Airflow DAG structure](images/airflow_dag_graph.png)

### Successful DAG run
![Airflow successful run](images/airflow_success_run.png)

## Bronze and Silver validation

The pipeline lands raw OpenAQ data in the Bronze layer, transforms it into curated Silver parquet datasets, and validates data quality before warehouse loading.

### Bronze ingestion success
![Bronze ingestion success](images/bronze_ingestion_success.png)

### Silver quality report
![Silver quality report](images/silver_quality_report.png)

## dbt

### dbt run output
![dbt run output](images/dbt_run_output.png)

### dbt test output
![dbt test output](images/dbt_test_output.png)

## BigQuery

The warehouse and analytical marts are materialized in BigQuery. Cloud-side evidence is already captured below through the load and table screenshots committed in `docs/images/`.

### BigQuery load output
![BigQuery load output](images/load_to_bigquery.png)

### BigQuery tables
![BigQuery tables](images/bigquery_tables.png)

## GCS staging

The warehouse loader stages the Silver parquet dataset in GCS before the
BigQuery load step. In `warehouse/load_to_bigquery.py`, the local Silver dataset
at `data/silver/air_quality_measurements` is copied to:

`gs://<configured-bucket>/silver/air_quality_measurements`

That staged path is then used as the source for the `bq load` command.

### GCS Silver staging evidence gap

A committed GCS bucket screenshot is still missing from `docs/images/`. Capture
it after the next authenticated load and save it as
`docs/images/gcs_silver_staging.png`.

Suggested command:

```bash
gcloud storage ls --long gs://<configured-bucket>/silver/air_quality_measurements/
```

If you prefer `gsutil`, this also works:

```bash
gsutil ls -lh gs://<configured-bucket>/silver/air_quality_measurements/
```

## Data quality numbers

The latest local Silver quality report available in this workspace showed a
passing run, and the values are copied below for reviewer convenience:

```json
{
  "status": "pass",
  "silver_dir": "data/silver/air_quality_measurements",
  "row_count": 185473,
  "cities": [
    "Beijing",
    "Berlin",
    "Delhi",
    "London",
    "New York"
  ],
  "pollutants": [
    "no2",
    "o3",
    "pm10",
    "pm25"
  ],
  "duplicate_count": 0,
  "null_checks": {
    "city": 0,
    "location_id": 0,
    "pollutant": 0,
    "measurement_value": 0,
    "measurement_datetime": 0
  },
  "errors": []
}
```

Supplementary row distribution from the latest local Silver run summary in this
workspace:

```json
{
  "city_counts": {
    "Beijing": 37252,
    "Berlin": 49165,
    "Delhi": 18863,
    "London": 43023,
    "New York": 37170
  },
  "date_range": {
    "min": "2023-12-31T19:30:00",
    "max": "2026-03-11T18:30:00"
  }
}
```

## dbt test summary

The committed dbt artifacts under `dbt/air_quality_project/` show a passing test
run generated on `2026-03-14T22:42:36.988218Z`.

Summary from `dbt/air_quality_project/logs/dbt.log` and
`dbt/air_quality_project/target/run_results.json`:

```text
Finished running 25 data tests in 0 hours 0 minutes and 6.64 seconds.
Completed successfully
Done. PASS=25 WARN=0 ERROR=0 SKIP=0 NO-OP=0 TOTAL=25
```

## Dashboard

The final dashboard presents a five-city comparison of pollution trends and pollutant patterns.

### Dashboard overview
![Dashboard overview](images/dashboard_overview.png)

### Dashboard export
[Global City Air Quality Observatory dashboard PDF](images/Global_City_Air_Quality_Observatory_Dashboard.pdf)

### Live dashboard
[Global City Air Quality Observatory Looker Studio dashboard](https://lookerstudio.google.com/reporting/6432e2e1-4363-493c-bbf8-598c60bb49de)
