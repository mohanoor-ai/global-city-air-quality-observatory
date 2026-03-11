# Airflow DAGs

This folder contains two simple DAG entrypoints:

- `air_quality_backfill_pipeline_dag` (manual trigger, no schedule)
- `air_quality_daily_pipeline_dag` (scheduled `@daily`)

Both DAGs run the same task chain:

`ingest_bronze -> build_silver -> data_quality_gate -> load_warehouse -> dbt_run -> dbt_test`

The only difference is ingestion mode:

- backfill DAG runs `--mode backfill`
- daily DAG runs `--mode daily`

## Notes

- DAG file: `airflow/air_quality_pipeline_dag.py`
- Project root in DAG: `/home/moha_/projects/air-quality-data-pipeline`
