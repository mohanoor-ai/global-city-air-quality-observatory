"""Airflow DAGs for the five-city end-to-end batch pipeline."""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


PROJECT_ROOT = "/home/moha_/projects/air-quality-data-pipeline"

default_args = {
    "owner": "global-city-air-quality-observatory",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


def add_pipeline_tasks(dag: DAG, ingestion_mode: str) -> None:
    resolve_scope_and_window = BashOperator(
        task_id="resolve_scope_and_window",
        bash_command=(
            f"cd {PROJECT_ROOT} && "
            "uv run python main.py show-scope"
        ),
        dag=dag,
    )

    download_raw_archive_files = BashOperator(
        task_id="download_raw_archive_files",
        bash_command=(
            f"cd {PROJECT_ROOT} && "
            f"uv run python ingestion/download_air_quality_data.py --mode {ingestion_mode}"
        ),
        dag=dag,
    )

    store_bronze_files = BashOperator(
        task_id="store_bronze_files",
        bash_command=(
            f"cd {PROJECT_ROOT} && "
            "uv run python main.py verify-bronze"
        ),
        dag=dag,
    )

    run_spark_bronze_to_silver = BashOperator(
        task_id="run_spark_bronze_to_silver",
        bash_command=(
            f"cd {PROJECT_ROOT} && "
            "uv run python spark/bronze_to_silver.py "
            f"--write-mode {'overwrite' if ingestion_mode == 'backfill' else 'append'}"
        ),
        dag=dag,
    )

    run_silver_quality_checks = BashOperator(
        task_id="run_silver_quality_checks",
        bash_command=(
            f"cd {PROJECT_ROOT} && "
            "uv run python spark/check_silver_data_quality.py"
        ),
        dag=dag,
    )

    load_warehouse = BashOperator(
        task_id="load_silver_to_bigquery",
        bash_command=(
            f"cd {PROJECT_ROOT} && "
            "uv run python warehouse/load_to_bigquery.py"
        ),
        dag=dag,
    )

    run_dbt_staging = BashOperator(
        task_id="run_dbt_staging",
        bash_command=(
            f"cd {PROJECT_ROOT} && "
            ".venv-dbt/bin/dbt run --project-dir dbt/air_quality_project --select stg_air_quality"
        ),
        dag=dag,
    )

    run_dbt_marts = BashOperator(
        task_id="run_dbt_marts",
        bash_command=(
            f"cd {PROJECT_ROOT} && "
            "bash scripts/dbt_run.sh"
        ),
        dag=dag,
    )

    run_validation_checks = BashOperator(
        task_id="run_validation_checks",
        bash_command=(
            f"cd {PROJECT_ROOT} && "
            "bash scripts/dbt_test.sh"
        ),
        dag=dag,
    )

    finish_pipeline = BashOperator(
        task_id="finish_pipeline",
        bash_command=(
            f"cd {PROJECT_ROOT} && "
            "uv run python main.py verify-quality-report"
        ),
        dag=dag,
    )

    (
        resolve_scope_and_window
        >> download_raw_archive_files
        >> store_bronze_files
        >> run_spark_bronze_to_silver
        >> run_silver_quality_checks
        >> load_warehouse
        >> run_dbt_staging
        >> run_dbt_marts
        >> run_validation_checks
        >> finish_pipeline
    )


backfill_dag = DAG(
    dag_id="global_city_air_quality_backfill",
    default_args=default_args,
    start_date=datetime(2026, 3, 9),
    schedule=None,
    catchup=False,
    tags=["air-quality", "batch", "backfill"],
)

daily_dag = DAG(
    dag_id="global_city_air_quality_daily",
    default_args=default_args,
    start_date=datetime(2026, 3, 9),
    schedule="@daily",
    catchup=False,
    tags=["air-quality", "batch", "daily"],
)

add_pipeline_tasks(backfill_dag, ingestion_mode="backfill")
add_pipeline_tasks(daily_dag, ingestion_mode="daily")
