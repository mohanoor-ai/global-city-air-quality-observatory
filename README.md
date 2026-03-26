# Global City Air Quality Observatory

This project compares air pollution trends and pollutant patterns across
London, New York, Delhi, Beijing, and Berlin.

## Problem Statement

Air quality affects public health, transport, and city policy, but the patterns
are different from city to city. This project builds a batch pipeline that
pulls [OpenAQ archive data](https://docs.openaq.org/aws/about), prepares it
for analysis, and shows cross-city trends in a dashboard.

Comparing air pollution across cities is harder than it should be because:

- raw air-quality data is difficult to use directly for analysis
- data from different cities is not always structured consistently
- comparing pollution trends across cities takes too much manual work
- decision-makers need a reliable way to monitor city-level air-quality patterns
- there is no simple end-to-end view that turns raw data into dashboard-ready insights

This project solves that by building a batch pipeline that collects
[OpenAQ archive data](https://docs.openaq.org/aws/about), standardizes it, and
presents cross-city trends in a dashboard.

## Why Partitioning, Clustering, and dbt Matter

The fact table is partitioned by `measurement_date` and clustered by `city` and
`pollutant` because the project constantly filters by time, city, and
pollutant. dbt sits on top of that warehouse layer to build
reviewer-friendly reporting tables instead of leaving all analysis at raw
measurement grain.

## Scope and Cities

The project is intentionally limited to five cities:

- London
- New York
- Delhi
- Beijing
- Berlin

The fixed scope is stored in
[ingestion/location_targets.csv](ingestion/location_targets.csv).

## Architecture Summary

Source data: [OpenAQ archive](https://docs.openaq.org/aws/about)

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
[airflow/dags/global_city_air_quality_observatory_dag.py](airflow/dags/global_city_air_quality_observatory_dag.py).

The DAG runs this flow:

1. validate city scope
2. download Bronze data
3. verify Bronze coverage
4. transform Bronze to Silver
5. run Silver quality checks
6. load BigQuery warehouse tables
7. run dbt models
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
├── .github/
│   └── workflows/tests.yml
├── airflow/
│   ├── Dockerfile
│   └── dags/global_city_air_quality_observatory_dag.py
├── ingestion/
│   ├── download_air_quality_data.py
│   └── location_targets.csv
├── spark/
│   ├── bronze_to_silver.py
│   └── check_silver_data_quality.py
├── warehouse/
│   └── load_to_bigquery.py
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

2. Install `gcloud`, then authenticate and select your project.

```bash
curl https://sdk.cloud.google.com | bash
gcloud version
gcloud auth login
gcloud auth application-default login
gcloud config set project <your-gcp-project-id>
```

3. Copy [`.env.example`](.env.example) to `.env`, save your GCP service account
key JSON locally, and set:

```bash
cp .env.example .env
```

- `GCP_PROJECT_ID`
- `GCS_BUCKET_NAME`
- `GOOGLE_APPLICATION_CREDENTIALS=/absolute/path/to/your-gcp-key.json`

4. Create Terraform variables from
[terraform/terraform.tfvars.example](terraform/terraform.tfvars.example) and
provision infrastructure.

```bash
cp terraform/terraform.tfvars.example terraform/terraform.tfvars
cd terraform
terraform init
terraform apply -var-file=terraform.tfvars
cd ..
```

5. Run the pipeline from the repo root.

```bash
make run
```

Optional Airflow:

```bash
make airflow-init
make airflow-start
```

Airflow UI: `http://localhost:8080`

If you are using WSL with Docker Desktop, enable WSL integration for this
distro before running the Airflow targets.

## Reproducibility

- Fastest review path: read [docs/review-guide.md](docs/review-guide.md), then [docs/execution-evidence.md](docs/execution-evidence.md), then open the dashboard screenshot and PDF.
- Local code verification is available with `make test` and does not require GCP credentials.
- A full end-to-end rerun requires `gcloud`, Terraform, Docker Compose, and access to the configured GCP project, GCS bucket, and BigQuery datasets.
- For local Airflow review, make sure `.env` includes `GCP_PROJECT_ID`, `GCS_BUCKET_NAME`, and `GOOGLE_APPLICATION_CREDENTIALS`.

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

- Latest committed run evidence in this repo is from March 14, 2026.
- Reproducibility notes: [docs/review-guide.md](docs/review-guide.md)
- Execution evidence: [docs/execution-evidence.md](docs/execution-evidence.md)

## Dashboard

![Dashboard overview](docs/images/dashboard_overview.png)

- Live dashboard: [Looker Studio report](https://lookerstudio.google.com/reporting/6432e2e1-4363-493c-bbf8-598c60bb49de)
- PDF export: [docs/images/Global_City_Air_Quality_Observatory_Dashboard.pdf](docs/images/Global_City_Air_Quality_Observatory_Dashboard.pdf)
