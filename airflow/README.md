# Airflow DAGs

This folder contains two DAG entrypoints:

- `global_city_air_quality_backfill`
- `global_city_air_quality_daily`

Both DAGs orchestrate the same end-to-end flow:

`resolve_scope_and_window -> download_raw_archive_files -> store_bronze_files -> run_spark_bronze_to_silver -> run_silver_quality_checks -> load_silver_to_bigquery -> run_dbt_staging -> run_dbt_marts -> run_validation_checks -> finish_pipeline`

The only difference is ingestion mode:

- backfill DAG runs `--mode backfill`
- daily DAG runs `--mode daily`

Notes:

- DAG file: `airflow/air_quality_pipeline_dag.py`
- project root in DAG: `/home/moha_/projects/air-quality-data-pipeline`
