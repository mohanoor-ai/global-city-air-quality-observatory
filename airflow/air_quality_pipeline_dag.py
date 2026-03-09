"""
Airflow DAG for the Air Quality batch pipeline.

Pipeline order:
1. Build Silver dataset
2. Run data quality gate
3. Load data into BigQuery warehouse
"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


PROJECT_ROOT = "/home/moha_/projects/air-quality-data-pipeline"

default_args = {
    "owner": "air-quality-pipeline",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="air_quality_pipeline_dag",
    default_args=default_args,
    start_date=datetime(2026, 3, 9),
    schedule="@daily",
    catchup=False,
    tags=["air-quality", "batch"],
) as dag:
    build_silver = BashOperator(
        task_id="build_silver",
        bash_command=(
            f"cd {PROJECT_ROOT} && "
            "uv run python processing/clean_air_quality_data.py"
        ),
    )

    data_quality_gate = BashOperator(
        task_id="data_quality_gate",
        bash_command=(
            f"cd {PROJECT_ROOT} && "
            "uv run python processing/check_silver_data_quality.py"
        ),
    )

    load_warehouse = BashOperator(
        task_id="load_warehouse",
        bash_command=(
            f"cd {PROJECT_ROOT} && "
            "uv run python warehouse/load_to_bigquery.py"
        ),
    )

    build_silver >> data_quality_gate >> load_warehouse
