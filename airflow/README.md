# Airflow DAGs

This folder contains two DAG entrypoints:

- `global_city_air_quality_backfill`
- `global_city_air_quality_daily`

Both DAGs orchestrate the same end-to-end flow:

`show_scope -> download_data -> verify_bronze -> bronze_to_silver -> silver_data_quality -> load_bigquery -> dbt_run -> dbt_test -> verify_quality_report`

The only difference is ingestion mode:

- backfill DAG runs `--mode backfill`
- daily DAG runs `--mode daily`

Notes:

- DAG file: `airflow/global_city_air_quality_observatory_dag.py`
- project root in DAG: resolved dynamically from the DAG file location
