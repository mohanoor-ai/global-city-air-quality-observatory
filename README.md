# Global City Air Quality Observatory

Batch data engineering project comparing air pollution trends and pollutant patterns across London, New York, Delhi, Beijing, and Berlin using GCP, Airflow, Spark, BigQuery, dbt, and Looker Studio.

## Quick links

- Architecture diagram: `docs/images/architecture_diagram.svg`
- Runbook: `runbook.md`
- Reviewer guide: `docs/review-guide.md`
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

This project uses a fixed five-city scope to stay focused, reviewer-friendly, and reproducible. The goal is not global ranking. The goal is a consistent five-city comparison built as an end-to-end batch data engineering project.

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
- `docs/` - reviewer guide, architecture decisions, execution evidence, dashboard design
- `tests/` - validation checks
- `scripts/` - helper scripts for dbt execution and local Airflow startup
- `requirements.txt` - reviewer-friendly pip install snapshot generated from `uv.lock`

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
- [airflow/global_city_air_quality_observatory_dag.py](airflow/global_city_air_quality_observatory_dag.py)

Spark is the official Bronze to Silver transformation engine in this repository.

## Airflow orchestration

The repository contains Airflow DAGs for:

- backfill runs
- daily runs

For local DAG runs, Airflow should be installed in a dedicated environment. It is not installed by `uv sync` for the main project environment.

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

This keeps the orchestration easy to review from source download through warehouse loading, dbt transformation, and final validation.

## Warehouse loading and modeling

The warehouse layer is implemented in BigQuery and is designed for analytical querying and dashboard use.

- the fact table is partitioned by date using `measurement_date`
- the fact table is clustered by `city` and `pollutant`
- supporting dimensions make reporting and filtering easier
- dbt builds analytical marts from warehouse data for dashboard use

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

Dashboard preview:

![Global City Air Quality Observatory dashboard preview](docs/images/dashboard_overview.png)

## How to run from zero

### Prerequisites

- Python `3.11` to `3.13`
- Java 17
- `uv` for the development workflow, or `pip` with `requirements.txt` for reviewer setup
- Google Cloud credentials
- Terraform
- dedicated Airflow environment for local DAG runs
- dbt environment

### Setup

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

Configure environment variables and Google Cloud credentials, then provision infrastructure.

If you want to run Airflow locally, install it separately and use the helper script:

```bash
uv venv .venv-airflow --python 3.11
source .venv-airflow/bin/activate
uv pip install apache-airflow
bash scripts/airflow_standalone.sh
```

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

### Reviewer-facing outputs

- Airflow DAG evidence
- dbt execution evidence
- warehouse evidence
- dashboard evidence

## Evidence for reviewers

Reviewer-facing evidence is available in:

- `docs/execution-evidence.md`
- `docs/review-guide.md`

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

## Reviewer guide

- [docs/review-guide.md](docs/review-guide.md)

## Proof of run

- [docs/execution-evidence.md](docs/execution-evidence.md)
