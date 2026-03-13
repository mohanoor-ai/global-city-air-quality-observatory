# Runbook

## Prerequisites

- Python `3.11` to `3.13`
- Java 17 available for local Spark
- `uv` installed
- GCP project, billing, and BigQuery enabled
- `gcloud`, `bq`, and Terraform installed
- dbt environment available at `.venv-dbt`
- Airflow installed in the environment you use for DAG testing

GCP auth requirements:

```bash
gcloud auth login
gcloud auth application-default login
```

## Setup

1. Clone the repo and install dependencies.

```bash
uv sync
cp .env.example .env
```

2. Configure environment variables in `.env`.

Important values:

- `PROJECT_ID`
- `GCS_BUCKET`
- `BIGQUERY_DATASET`
- `JAVA_HOME`
- `AIRFLOW_HOME`

3. Apply Terraform to provision the GCS Bronze and Silver prefixes plus the BigQuery dataset and base warehouse tables.

```bash
cd terraform
terraform init
terraform plan -var-file=terraform.tfvars
terraform apply -var-file=terraform.tfvars
cd ..
```

4. Initialize Airflow if needed.

```bash
airflow db init
airflow users create --username admin --firstname admin --lastname admin --role Admin --email admin@example.com --password admin
```

Terraform creates:

- one GCS bucket for the data lake
- `bronze/` and `silver/` object prefixes
- one BigQuery dataset for the warehouse
- the partitioned and clustered fact table
- the `dim_city` and `dim_pollutant` helper dimensions

## Execution

Run the pipeline stage by stage from the repo root.

1. Ingestion to Bronze

```bash
uv run python ingestion/download_air_quality_data.py --mode backfill
```

2. Spark Bronze to Silver

```bash
uv run python spark/bronze_to_silver.py --write-mode overwrite
```

3. Silver quality checks

```bash
uv run python spark/check_silver_data_quality.py
```

4. Load Silver to BigQuery

```bash
uv run python warehouse/load_to_bigquery.py
```

5. Run dbt models and tests

```bash
bash scripts/dbt_run.sh
bash scripts/dbt_test.sh
```

6. Run the daily refresh flow

```bash
uv run python ingestion/download_air_quality_data.py --mode daily
uv run python spark/bronze_to_silver.py --write-mode append
uv run python spark/check_silver_data_quality.py
uv run python warehouse/load_to_bigquery.py
```

7. Run Airflow DAGs

Backfill DAG: `global_city_air_quality_backfill`

Daily DAG: `global_city_air_quality_daily`

## Validation

Expected local outputs:

- `data/bronze/` raw archive files
- `data/bronze/location_metadata.csv`
- `data/silver/air_quality_measurements/`
- `data/silver/latest_run_summary.json`
- `data/quality/silver_dq_report.json`

Expected BigQuery tables:

- `air_quality_dw.fct_air_quality_measurements`
- `air_quality_dw.dim_city`
- `air_quality_dw.dim_pollutant`
- dbt marts in schema `marts`

Sample validation SQL:

```sql
SELECT COUNT(*) FROM `your-project.air_quality_dw.fct_air_quality_measurements`;

SELECT measurement_date, city, pollutant, COUNT(*) AS row_count
FROM `your-project.air_quality_dw.fct_air_quality_measurements`
GROUP BY 1, 2, 3
ORDER BY measurement_date DESC, city, pollutant;

SELECT * FROM `your-project.marts.mart_pm25_city_daily`
ORDER BY measurement_date DESC, city
LIMIT 20;
```

Expected dbt result:

- `stg_air_quality` builds successfully
- all marts in `dbt/air_quality_project/models/marts/reporting/` build successfully
- `dbt test` passes the not-null and accepted-values checks

Expected DAG result:

- each task succeeds from scope resolution through validation
- screenshots can be stored at [images/airflow_backfill_success.png](/home/moha_/projects/global-city-air-quality-observatory/images/airflow_backfill_success.png)

## Dashboard access

Connect Looker Studio to the BigQuery marts dataset and use the tile mapping in [dashboards/README.md](/home/moha_/projects/global-city-air-quality-observatory/dashboards/README.md).
