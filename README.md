# Global City Air Quality Observatory

Batch data engineering project comparing air pollution trends and pollutant patterns across London, New York, Delhi, Beijing, and Berlin using GCP, Airflow, Spark, BigQuery, dbt, and Looker Studio.

## Quick links

- Reviewer guide: `docs/review-guide.md`
- Architecture diagram: `docs/images/architecture_diagram.svg`
- Runbook: `runbook.md`
- Project guide: `docs/project-guide.md`
- Proof of run: `docs/execution-evidence.md`
- Dashboard documentation: `docs/dashboard-design.md`
- Live dashboard: `https://lookerstudio.google.com/reporting/6432e2e1-4363-493c-bbf8-598c60bb49de`

## Problem statement

This project answers a focused analytics question:

**How do pollution trends and pollutant patterns differ across five major global cities over time?**

It is designed as an end-to-end batch data engineering project that clearly shows:

1. where the data comes from
2. how it lands in the data lake
3. how it moves into the warehouse
4. how it is transformed
5. how it is visualized
6. how someone else can run it

This project compares:

- London
- New York
- Delhi
- Beijing
- Berlin

## Why these five cities

Air pollution is a meaningful cross-city comparison problem because the same pollutants can behave differently across places, seasons, and monitoring environments.

This project uses a fixed five-city scope to stay focused, clear, and reproducible. The goal is not global ranking. The goal is a consistent five-city comparison built as an end-to-end batch data engineering project.

## Data source and scope

The dataset comes from OpenAQ archive/source data and is intentionally restricted to a fixed five-city comparison for consistency and reproducibility.

This project is intentionally limited to these five cities only:

- London
- New York
- Delhi
- Beijing
- Berlin

The single source of truth for project scope is `ingestion/location_targets.csv`.

## Architecture

```text
OpenAQ source data
-> Local Bronze landing in data/bronze
-> Spark Bronze to Silver transformation
-> Silver staged to GCS for BigQuery loading
-> BigQuery warehouse loading
-> dbt analytical marts
-> Looker Studio dashboard
```

Architecture diagram: [docs/images/architecture_diagram.svg](docs/images/architecture_diagram.svg)

## What this project demonstrates

This repository demonstrates a complete batch analytics pipeline using the following tools and platforms:

- Google Cloud Platform
- Terraform
- Apache Airflow
- Apache Spark
- Google Cloud Storage
- BigQuery
- dbt
- Looker Studio
- uv

## Repository structure

- `ingestion/` - source download, city scope, Bronze landing
- `spark/` - Bronze to Silver transformation and Silver quality checks
- `warehouse/` - BigQuery load logic
- `dbt/` - staging models and analytical marts
- `airflow/` - orchestration DAGs for backfill and daily runs
- `terraform/` - GCP infrastructure as code
- `docs/` - project guide, architecture decisions, execution evidence, dashboard design
- `tests/` - validation checks
- `scripts/` - helper scripts for dbt execution and repo utilities
- `requirements.txt` - pip install snapshot generated from `uv.lock`

## End-to-end pipeline flow

1. Download raw OpenAQ archive data for the five configured cities
2. Land raw files in the Bronze layer
3. Transform Bronze data into Silver parquet datasets using Spark
4. Run Silver data quality checks
5. Load curated warehouse data into BigQuery
6. Build reporting marts with dbt
7. Visualize five-city insights in Looker Studio

Main execution files:

- [main.py](main.py)
- [ingestion/download_air_quality_data.py](ingestion/download_air_quality_data.py)
- [spark/bronze_to_silver.py](spark/bronze_to_silver.py)
- [spark/check_silver_data_quality.py](spark/check_silver_data_quality.py)
- [warehouse/load_to_bigquery.py](warehouse/load_to_bigquery.py)
- [airflow/dags/global_city_air_quality_observatory_dag.py](airflow/dags/global_city_air_quality_observatory_dag.py)

Spark is the official Bronze to Silver transformation engine in this repository.

## Airflow orchestration

The repository contains Airflow DAGs for:

- backfill runs
- daily runs

For local DAG runs, Airflow uses the official Docker Compose stack committed at
`docker-compose.yaml`.

The compose stack builds a project-specific Airflow image from
`airflow/Dockerfile`, so the containers include the runtime tools this pipeline
needs such as Java, Google Cloud SDK, Python dependencies, and dbt.

The exact DAG task flow is:

- `show_scope`
- `download_data`
- `verify_bronze`
- `bronze_to_silver`
- `silver_data_quality`
- `load_bigquery`
- `dbt_run`
- `dbt_test`
- `verify_quality_report`

This keeps the orchestration easy to inspect from source download through warehouse loading, dbt transformation, and final validation.

## Warehouse loading and modeling

The warehouse layer is implemented in BigQuery and is designed for analytical querying and dashboard use.

- the fact table is partitioned by date using `measurement_date`
- the fact table is clustered by `city` and `pollutant`
- supporting dimensions make reporting and filtering easier
- dbt builds analytical marts from warehouse data for dashboard use

### BigQuery fact table schema

| Column | Type | Notes |
|---|---|---|
| `city` | STRING | One of the five scoped cities |
| `country` | STRING | Two-letter country code from the scoped source |
| `location_id` | INT64 | OpenAQ location identifier |
| `location_name` | STRING | Human-readable monitoring location name |
| `sensor_id` | INT64 | Sensor identifier when available |
| `pollutant` | STRING | Lower-cased pollutant code such as `pm25`, `pm10`, `no2`, `co`, `o3` |
| `measurement_value` | FLOAT64 | Standardized measurement value |
| `measurement_unit` | STRING | Measurement unit from the source |
| `measurement_datetime` | TIMESTAMP | Source event timestamp |
| `measurement_date` | DATE | Partition key |
| `latitude` | FLOAT64 | Source latitude when available |
| `longitude` | FLOAT64 | Source longitude when available |
| `batch_date` | DATE | Batch partition carried from the Silver layer |
| `source_file` | STRING | Bronze source filename for lineage |

Supporting dimension tables: `dim_city`, `dim_pollutant`

## Dashboard story

The dashboard is a focused five-city comparison dashboard for:

- London
- New York
- Delhi
- Beijing
- Berlin

It focuses on:

- city trend over time
- pollutant distribution by city
- cross-city comparison
- extreme pollution events within the five selected cities

Dashboard resources:

- Documentation: `docs/dashboard-design.md`
- Live dashboard: `https://lookerstudio.google.com/reporting/6432e2e1-4363-493c-bbf8-598c60bb49de`
- Evidence screenshots: `docs/execution-evidence.md`
- PDF export: `docs/images/Global_City_Air_Quality_Observatory_Dashboard.pdf`

If the live dashboard is unavailable or still restricted by sharing settings,
use the committed PDF export as the fallback review artifact.

Dashboard preview:

![Global City Air Quality Observatory dashboard preview](docs/images/dashboard_overview.png)

## How to run from zero

### Prerequisites

- Python `3.11` to `3.13`
- Java 17
- `uv` for the development workflow, or `pip` with `requirements.txt` as an optional installation path
- Google Cloud credentials
- Terraform
- Docker and Docker Compose for local Airflow orchestration

### Environment model

- One local Python environment powers manual pipeline commands and dbt
- Docker Compose runs Airflow separately for orchestration

### Setup

For development, keep using `uv`:

```bash
uv sync
```

This installs the project dependencies for ingestion, Spark helpers, warehouse
loading, and dbt into the same local Python environment.

If you prefer not to use `uv`:

```bash
python -m venv .venv-pip
source .venv-pip/bin/activate
python -m pip install -r requirements.txt
```

Configure environment variables and Google Cloud credentials, then provision infrastructure.

If you want to run Airflow locally, copy `.env.example` to `.env`, update the
GCP values and credential path, then start the official compose stack:

```bash
cp .env.example .env
make airflow-init
make airflow-start
```

The first Docker-based Airflow run may take several minutes because it builds
the custom image before starting the services.

If you are using WSL with Docker Desktop, enable WSL integration for this
distro so `docker compose` is available from the shell that runs the Makefile.

```bash
cd terraform
terraform init
terraform plan -var-file=terraform.tfvars
terraform apply -var-file=terraform.tfvars
cd ..
```

### Manual pipeline run

If you installed dependencies with `requirements.txt` in an activated virtualenv, replace each `uv run python` command below with `python`.

```bash
uv run python main.py show-scope
uv run python ingestion/download_air_quality_data.py --mode backfill
uv run python main.py verify-bronze
uv run python spark/bronze_to_silver.py --write-mode overwrite
uv run python spark/check_silver_data_quality.py
uv run python warehouse/load_to_bigquery.py
bash scripts/dbt_run.sh
bash scripts/dbt_test.sh
uv run python main.py verify-quality-report
```

### Full run instructions

See `runbook.md` for setup details, Airflow startup, DAG execution, and validation steps.

## Expected outputs

Successful runs should produce:

### Local outputs

- Bronze raw files
- Silver parquet datasets
- Silver run summary
- Silver data quality report

### Warehouse outputs

- curated BigQuery fact table
- supporting BigQuery dimensions
- dbt reporting marts

### Documentation outputs

- Airflow DAG evidence
- dbt execution evidence
- warehouse evidence
- dashboard evidence

## Reviewer guide and evidence

Project documentation and evidence are available in:

- `docs/review-guide.md`
- `docs/execution-evidence.md`
- `docs/project-guide.md`

Evidence included there:

- Airflow DAG screenshot
- Bronze ingestion screenshot
- Silver quality report screenshot or JSON excerpt
- BigQuery load screenshot
- BigQuery tables screenshot
- dbt run/test output screenshot
- dashboard screenshot

## Lessons learned

Keeping the scope fixed to five cities made the project easier to explain, validate, and dashboard cleanly. Spark became the right choice once the Bronze to Silver step needed schema enforcement, metadata enrichment, deduplication, and repeatable parquet output. BigQuery partitioning and clustering mattered because the project constantly filters by date, city, and pollutant.

## Architecture decisions

- [docs/architecture-decisions.md](docs/architecture-decisions.md)

## Project guide

- [docs/project-guide.md](docs/project-guide.md)

## Reviewer guide

- [docs/review-guide.md](docs/review-guide.md)

## Proof of run

- [docs/execution-evidence.md](docs/execution-evidence.md)
