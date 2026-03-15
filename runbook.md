# Runbook

## Prerequisites

- Python `3.11` to `3.13`
- Java 17 for local Spark
- `uv` for the development workflow, or `pip` with `requirements.txt` for reviewer setup
- `gcloud`
- `bq`
- Terraform
- an available Airflow environment
- a dbt environment at `.venv-dbt`

## Setup

1. Install project dependencies.

For development, keep using `uv`:

```bash
uv sync
```

For reviewer-friendly installation without `uv`:

```bash
python -m venv .venv-review
source .venv-review/bin/activate
python -m pip install -r requirements.txt
```

2. Authenticate to GCP.

```bash
gcloud auth login
gcloud auth application-default login
```

3. Provision cloud resources.

```bash
cd terraform
terraform init
terraform plan -var-file=terraform.tfvars
terraform apply -var-file=terraform.tfvars
cd ..
```

4. Confirm or update the dbt profile in `dbt/air_quality_project/profiles.yml.example` and create your working profile.

5. Initialize Airflow if you want to run the DAG locally. Airflow is not installed by `uv sync`, so use a dedicated environment for it.

```bash
uv venv .venv-airflow --python 3.11
source .venv-airflow/bin/activate
uv pip install apache-airflow
bash scripts/airflow_standalone.sh
```

## Pipeline Flow

The Airflow DAG in [airflow/global_city_air_quality_observatory_dag.py](airflow/global_city_air_quality_observatory_dag.py) orchestrates this exact flow:

1. `show_scope`
2. `download_data`
3. `verify_bronze`
4. `bronze_to_silver`
5. `silver_data_quality`
6. `load_bigquery`
7. `dbt_run`
8. `dbt_test`
9. `verify_quality_report`

## Run Stage By Stage

Run the same flow manually from the repo root if needed.

If you installed dependencies from `requirements.txt` in an activated virtualenv, replace each `uv run python` command below with `python`.

1. Show the fixed five-city scope.

```bash
uv run python main.py show-scope
```

2. Download OpenAQ archive files into Bronze.

```bash
uv run python ingestion/download_air_quality_data.py --mode backfill
```

3. Verify Bronze files exist.

```bash
uv run python main.py verify-bronze
```

4. Transform Bronze to Silver with Spark.

```bash
uv run python spark/bronze_to_silver.py --write-mode overwrite
```

5. Run Silver data quality checks.

```bash
uv run python spark/check_silver_data_quality.py
```

6. Load Silver data into BigQuery.

```bash
uv run python warehouse/load_to_bigquery.py
```

7. Run dbt models.

```bash
bash scripts/dbt_run.sh
```

8. Run dbt tests.

```bash
bash scripts/dbt_test.sh
```

9. Verify the final quality report.

```bash
uv run python main.py verify-quality-report
```

Those commands map directly to the DAG task names:

- `show_scope`
- `download_data`
- `verify_bronze`
- `bronze_to_silver`
- `silver_data_quality`
- `load_bigquery`
- `dbt_run`
- `dbt_test`
- `verify_quality_report`

## Daily Refresh Variant

For the daily batch flow, replace the ingestion and Spark write mode with:

```bash
uv run python ingestion/download_air_quality_data.py --mode daily
uv run python spark/bronze_to_silver.py --write-mode append
```

## Expected Outputs

Local outputs:

- `data/bronze/`
- `data/bronze/location_metadata.csv`
- `data/silver/air_quality_measurements/`
- `data/silver/latest_run_summary.json`
- `data/quality/silver_dq_report.json`

Warehouse outputs:

- `air_quality_dw.fct_air_quality_measurements`
- `air_quality_dw.dim_city`
- `air_quality_dw.dim_pollutant`
- dbt reporting marts

## Airflow

The repo includes two DAG entry points:

- `global_city_air_quality_backfill`
- `global_city_air_quality_daily`

Both use [airflow/global_city_air_quality_observatory_dag.py](airflow/global_city_air_quality_observatory_dag.py).

## Validation

Useful local validation command:

```bash
uv run python -m unittest -v tests/test_pipeline_checks.py
```

Useful warehouse validation files:

- [sql/warehouse_validation.sql](sql/warehouse_validation.sql)
- [sql/mart_validation.sql](sql/mart_validation.sql)
