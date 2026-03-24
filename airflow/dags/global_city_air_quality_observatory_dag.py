"""Airflow DAGs for the Global City Air Quality Observatory batch flow."""

from __future__ import annotations

from datetime import datetime, timedelta
import os
from pathlib import Path

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator


PROJECT_ROOT = os.getenv("PIPELINE_PROJECT_ROOT", str(Path(__file__).resolve().parents[2]))
DBT_PROJECT_ROOT = f"{PROJECT_ROOT}/dbt/air_quality_project"
TFVARS_FILE = f"{PROJECT_ROOT}/terraform/terraform.tfvars"
DBT_BIN = "/opt/airflow/.local/bin/dbt"

default_args = {
    "owner": "global-city-air-quality-observatory",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


def dbt_command(command: str) -> str:
    return (
        f"cd {DBT_PROJECT_ROOT} && "
        f"export DBT_PROFILES_DIR={DBT_PROJECT_ROOT} && "
        f"export PROJECT_ID=${{PROJECT_ID:-$(sed -n 's/^project_id[[:space:]]*=[[:space:]]*\"\\(.*\\)\"/\\1/p' {TFVARS_FILE} | head -n 1)}} && "
        f"export BIGQUERY_LOCATION=${{BIGQUERY_LOCATION:-$(sed -n 's/^bigquery_location[[:space:]]*=[[:space:]]*\"\\(.*\\)\"/\\1/p' {TFVARS_FILE} | head -n 1)}} && "
        "export DBT_DATASET=${DBT_DATASET:-air_quality_dbt} && "
        f"{DBT_BIN} {command} --project-dir . --profiles-dir ."
    )


def add_pipeline_tasks(dag: DAG, ingestion_mode: str) -> None:
    validate_city_scope = BashOperator(
        task_id="validate_city_scope",
        bash_command=f"cd {PROJECT_ROOT} && python ingestion/download_air_quality_data.py --validate-scope",
        dag=dag,
    )

    download_bronze_data = BashOperator(
        task_id="download_bronze_data",
        bash_command=(
            f"cd {PROJECT_ROOT} && "
            f"python ingestion/download_air_quality_data.py --mode {ingestion_mode}"
        ),
        dag=dag,
    )

    verify_bronze = BashOperator(
        task_id="verify_bronze",
        bash_command=f"cd {PROJECT_ROOT} && python ingestion/download_air_quality_data.py --verify-bronze",
        dag=dag,
    )

    bronze_to_silver = BashOperator(
        task_id="transform_bronze_to_silver",
        bash_command=(
            f"cd {PROJECT_ROOT} && "
            "python spark/bronze_to_silver.py --write-mode overwrite"
        ),
        dag=dag,
    )

    silver_data_quality = BashOperator(
        task_id="run_silver_quality_checks",
        bash_command=f"cd {PROJECT_ROOT} && python spark/check_silver_data_quality.py",
        dag=dag,
    )

    load_bigquery = BashOperator(
        task_id="load_bigquery_tables",
        bash_command=f"cd {PROJECT_ROOT} && python warehouse/load_to_bigquery.py",
        dag=dag,
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=dbt_command("run"),
        dag=dag,
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=dbt_command("test"),
        dag=dag,
    )

    verify_quality_report = BashOperator(
        task_id="verify_saved_quality_report",
        bash_command=f"cd {PROJECT_ROOT} && python spark/check_silver_data_quality.py --verify-report",
        dag=dag,
    )

    (
        validate_city_scope
        >> download_bronze_data
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
    max_active_runs=1,
    tags=["air-quality", "batch", "backfill"],
)

daily_dag = DAG(
    dag_id="global_city_air_quality_daily",
    default_args=default_args,
    start_date=datetime(2026, 3, 9),
    schedule="@daily",
    catchup=False,
    max_active_runs=1,
    tags=["air-quality", "batch", "daily"],
)

add_pipeline_tasks(backfill_dag, ingestion_mode="backfill")
add_pipeline_tasks(daily_dag, ingestion_mode="daily")
