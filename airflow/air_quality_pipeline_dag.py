"""
Airflow DAGs for the Air Quality batch pipeline.

Two entrypoints are provided:
- air_quality_backfill_pipeline_dag
- air_quality_daily_pipeline_dag
"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


PROJECT_ROOT = "/home/moha_/projects/air-quality-data-pipeline"
DBT_PROJECT_DIR = f"{PROJECT_ROOT}/dbt/air_quality_project"

default_args = {
    "owner": "air-quality-pipeline",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


def add_pipeline_tasks(dag: DAG, ingestion_mode: str) -> None:
    ingest = BashOperator(
        task_id="ingest_bronze",
        bash_command=(
            f"cd {PROJECT_ROOT} && "
            f"uv run python ingestion/download_air_quality_data.py --mode {ingestion_mode}"
        ),
        dag=dag,
    )

    build_silver = BashOperator(
        task_id="build_silver",
        bash_command=(
            f"cd {PROJECT_ROOT} && "
            "uv run python processing/clean_air_quality_data.py"
        ),
        dag=dag,
    )

    data_quality_gate = BashOperator(
        task_id="data_quality_gate",
        bash_command=(
            f"cd {PROJECT_ROOT} && "
            "uv run python processing/check_silver_data_quality.py"
        ),
        dag=dag,
    )

    load_warehouse = BashOperator(
        task_id="load_warehouse",
        bash_command=(
            f"cd {PROJECT_ROOT} && "
            "uv run python warehouse/load_to_bigquery.py"
        ),
        dag=dag,
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=(
            f"cd {DBT_PROJECT_DIR} && "
            "DBT_PROFILES_DIR=$(pwd) "
            "CLOUDSDK_CONFIG=/tmp/gcloud "
            "GOOGLE_APPLICATION_CREDENTIALS=/tmp/gcloud/application_default_credentials.json "
            f"{PROJECT_ROOT}/.venv-dbt/bin/dbt run"
        ),
        dag=dag,
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=(
            f"cd {DBT_PROJECT_DIR} && "
            "DBT_PROFILES_DIR=$(pwd) "
            "CLOUDSDK_CONFIG=/tmp/gcloud "
            "GOOGLE_APPLICATION_CREDENTIALS=/tmp/gcloud/application_default_credentials.json "
            f"{PROJECT_ROOT}/.venv-dbt/bin/dbt test"
        ),
        dag=dag,
    )

    ingest >> build_silver >> data_quality_gate >> load_warehouse >> dbt_run >> dbt_test


backfill_dag = DAG(
    dag_id="air_quality_backfill_pipeline_dag",
    default_args=default_args,
    start_date=datetime(2026, 3, 9),
    schedule=None,
    catchup=False,
    tags=["air-quality", "batch", "backfill"],
)

daily_dag = DAG(
    dag_id="air_quality_daily_pipeline_dag",
    default_args=default_args,
    start_date=datetime(2026, 3, 9),
    schedule="@daily",
    catchup=False,
    tags=["air-quality", "batch", "daily"],
)

add_pipeline_tasks(backfill_dag, ingestion_mode="backfill")
add_pipeline_tasks(daily_dag, ingestion_mode="daily")
