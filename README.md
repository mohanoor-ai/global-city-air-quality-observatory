# Global City Air Quality Observatory

This project compares air pollution trends and pollutant patterns across
London, New York, Delhi, Beijing, and Berlin.

## Problem Statement

Air quality affects public health, transport, and city policy, but the patterns
are different from city to city. This project builds a batch pipeline that
pulls OpenAQ archive data, prepares it for analysis, and shows cross-city
trends in a dashboard.

## Scope and Cities

The project is intentionally limited to five cities:

- London
- New York
- Delhi
- Beijing
- Berlin

The fixed scope is stored in `ingestion/location_targets.csv`.

## Architecture Summary

```text
OpenAQ archive
-> Bronze files in data/bronze
-> Spark Bronze to Silver parquet
-> Silver staged to GCS
-> BigQuery warehouse tables
-> dbt marts
-> Looker Studio dashboard
```

## Tech Stack

- Airflow for orchestration
- Terraform for GCP infrastructure
- Python and boto3 for ingestion
- Spark for Bronze to Silver transformation
- BigQuery for the warehouse
- dbt for analytical marts
- Looker Studio for the final dashboard
- Docker Compose for local Airflow

## Pipeline Flow

The official runtime path is the Airflow DAG in
`airflow/dags/global_city_air_quality_observatory_dag.py`.

The DAG runs this flow:

1. show the configured city scope
2. download OpenAQ archive files to Bronze
3. verify Bronze files exist for every configured city
4. transform Bronze to Silver with Spark
5. run Silver data quality checks
6. load Silver data to BigQuery
7. build dbt marts
8. run dbt tests
9. verify the saved quality report

## Repository Structure

```text
.
├── README.md
├── requirements.txt
├── .env.example
├── docker-compose.yml
├── Makefile
├── airflow/
│   ├── Dockerfile
│   └── dags/global_city_air_quality_observatory_dag.py
├── ingestion/
│   ├── city_scope.py
│   ├── download_air_quality_data.py
│   └── location_targets.csv
├── spark/
│   ├── bronze_to_silver.py
│   └── check_silver_data_quality.py
├── warehouse/load_to_bigquery.py
├── dbt/air_quality_project/
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── versions.tf
│   └── terraform.tfvars.example
├── docs/
│   ├── review-guide.md
│   ├── execution-evidence.md
│   └── images/
└── tests/test_pipeline_checks.py
```

## How to Run

1. Create a local environment and install dependencies.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Authenticate to GCP.

```bash
gcloud auth login
gcloud auth application-default login
```

3. Create Terraform variables and provision infrastructure.

```bash
cp terraform/terraform.tfvars.example terraform/terraform.tfvars
cd terraform
terraform init
terraform apply -var-file=terraform.tfvars
cd ..
```

4. For a manual end-to-end run from the repo root:

```bash
make run
```

5. For Airflow:

```bash
cp .env.example .env
make airflow-init
make airflow-start
```

Airflow UI: `http://localhost:8080`

If you are using WSL with Docker Desktop, enable WSL integration for this
distro before running the Airflow targets.

## Outputs

Local outputs:

- `data/bronze/records/csv.gz/...`
- `data/bronze/location_metadata.csv`
- `data/silver/air_quality_measurements/`
- `data/silver/latest_run_summary.json`
- `data/quality/silver_dq_report.json`

BigQuery tables:

- `air_quality_dw.fct_air_quality_measurements`
- `air_quality_dw.dim_city`
- `air_quality_dw.dim_pollutant`

dbt marts:

- `mart_city_pollution_trends`
- `mart_city_pollutant_distribution`
- `mart_city_extreme_events`
- `mart_city_comparison_summary`
- `mart_pm25_city_daily`

Dashboard outputs:

- live Looker Studio dashboard
- committed dashboard screenshot
- committed PDF export

## Proof and Evidence

- Reviewer guide: `docs/review-guide.md`
- Execution evidence: `docs/execution-evidence.md`

## Dashboard

![Dashboard overview](docs/images/dashboard_overview.png)

- Live dashboard: `https://lookerstudio.google.com/reporting/6432e2e1-4363-493c-bbf8-598c60bb49de`
- PDF export: `docs/images/Global_City_Air_Quality_Observatory_Dashboard.pdf`

## Why Partitioning, Clustering, and dbt Matter

The fact table is partitioned by `measurement_date` and clustered by `city` and
`pollutant` because the project constantly filters by time, city, and pollutant.
dbt sits on top of that warehouse layer to build reviewer-friendly reporting
tables instead of leaving all analysis at raw measurement grain.
