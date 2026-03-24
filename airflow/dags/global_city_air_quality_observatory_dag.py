"""Airflow DAGs for the end-to-end Global City Air Quality Observatory batch flow."""

from __future__ import annotations

from datetime import datetime, timedelta
import os
from pathlib import Path

from airflow import DAG
from airflow.operators.bash import BashOperator


def resolve_project_root() -> str:
    configured_root = os.getenv("PIPELINE_PROJECT_ROOT")
    if configured_root:
        return configured_root

    current_file = Path(__file__).resolve()
    for parent in current_file.parents:
        if (parent / "main.py").exists():
            return str(parent)

    return str(current_file.parents[1])


PROJECT_ROOT = resolve_project_root()

default_args = {
    "owner": "global-city-air-quality-observatory",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


def add_pipeline_tasks(dag: DAG, ingestion_mode: str) -> None:
    show_scope = BashOperator(
        task_id="show_scope",
        bash_command=f"cd {PROJECT_ROOT} && python main.py show-scope",
        dag=dag,
    )

    download_data = BashOperator(
        task_id="download_data",
        bash_command=(
            f"cd {PROJECT_ROOT} && "
            f"python ingestion/download_air_quality_data.py --mode {ingestion_mode}"
        ),
        dag=dag,
    )

    verify_bronze = BashOperator(
        task_id="verify_bronze",
        bash_command=f"cd {PROJECT_ROOT} && python main.py verify-bronze",
        dag=dag,
    )

    bronze_to_silver = BashOperator(
        task_id="bronze_to_silver",
        bash_command=(
            f"cd {PROJECT_ROOT} && "
            "python spark/bronze_to_silver.py "
            f"--write-mode {'overwrite' if ingestion_mode == 'backfill' else 'append'}"
        ),
        dag=dag,
    )

    silver_data_quality = BashOperator(
        task_id="silver_data_quality",
        bash_command=f"cd {PROJECT_ROOT} && python spark/check_silver_data_quality.py",
        dag=dag,
    )

    load_bigquery = BashOperator(
        task_id="load_bigquery",
        bash_command=f"cd {PROJECT_ROOT} && python warehouse/load_to_bigquery.py",
        dag=dag,
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {PROJECT_ROOT} && bash scripts/dbt_run.sh ",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"cd {PROJECT_ROOT} && bash scripts/dbt_test.sh ",
    )

    verify_quality_report = BashOperator(
        task_id="verify_quality_report",
        bash_command=f"cd {PROJECT_ROOT} && python main.py verify-quality-report",
        dag=dag,
    )

    (
        show_scope
        >> download_data
        >> verify_bronze
        >> bronze_to_silver
        >> silver_data_quality
        >> load_bigquery
        >> dbt_run
        >> dbt_test
        >> verify_quality_report
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
