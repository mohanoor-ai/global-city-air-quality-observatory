# Execution evidence

This document provides proof that the Global City Air Quality Observatory pipeline ran successfully across orchestration, transformation, warehouse loading, and visualization layers.

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

The warehouse and analytical marts are materialized in BigQuery.

### BigQuery load output
![BigQuery load output](images/load_to_bigquery.png)

### BigQuery tables
![BigQuery tables](images/bigquery_tables.png)

## Dashboard

The final dashboard presents a five-city comparison of pollution trends and pollutant patterns.

### Dashboard overview
![Dashboard overview](images/dashboard_overview.png)

### Dashboard export
[Global City Air Quality Observatory dashboard PDF](images/Global_City_Air_Quality_Observatory_Dashboard.pdf)

### Live dashboard
Add your Looker Studio link here.
