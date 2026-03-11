# Pipeline Orchestration

Airflow orchestration is intentionally simple.

## DAGs

- `air_quality_backfill_pipeline_dag`
- `air_quality_daily_pipeline_dag`

Both DAGs are defined in `airflow/air_quality_pipeline_dag.py`.

## Schedules

- Backfill DAG: `schedule=None` (manual trigger)
- Daily DAG: `@daily`

## Task Chain

Both DAGs run:

`ingest_bronze -> build_silver -> data_quality_gate -> load_warehouse -> dbt_run -> dbt_test`

Only `ingest_bronze` differs:

- backfill DAG runs `ingestion/download_air_quality_data.py --mode backfill`
- daily DAG runs `ingestion/download_air_quality_data.py --mode daily`

## Scope Notes

- Retry and monitoring stay at Airflow defaults with light tuning (`retries=1`).
- No sensors, branching, or dynamic task mapping are used in this version.
