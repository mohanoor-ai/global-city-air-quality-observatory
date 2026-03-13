# Global City Air Quality Observatory

Batch data engineering project comparing air pollution trends and pollutant patterns across London, New York, Delhi, Beijing, and São Paulo using GCP, Airflow, Spark, BigQuery, dbt, and Looker Studio.

## Problem Statement

Global City Air Quality Observatory is a batch data engineering project that compares air pollution trends and pollutant patterns across London, New York, Delhi, Beijing, and São Paulo using OpenAQ, GCS, Spark, BigQuery, dbt, Airflow, and Looker Studio.

The project question is:

How do pollution trends and pollutant patterns differ across five major global cities over time?

This repository is intentionally narrow. It tells one reviewer-friendly story from ingestion to dashboard instead of trying to cover every city in the archive.

## Scope

The project scope is fixed to exactly five cities:

- London
- New York
- Delhi
- Beijing
- São Paulo

These five cities provide geographic spread, strong analytical contrast, workable source coverage, and a capstone-sized scope that is realistic to validate and reproduce.

The single source of truth for scope is [ingestion/location_targets.csv](ingestion/location_targets.csv).

## Architecture

Official architecture story:

```text
OpenAQ source data
-> Bronze ingestion to Google Cloud Storage
-> Spark Bronze to Silver transformation
-> BigQuery warehouse loading
-> dbt analytical marts
-> Looker Studio dashboard
```

Architecture diagram: [images/architecture_diagram.svg](images/architecture_diagram.svg)

The pipeline is batch-first:

- Python downloads OpenAQ archive files for the fixed city scope.
- Bronze keeps raw files in GCS for traceability.
- Spark standardizes Bronze data into a Silver parquet dataset.
- BigQuery stores the warehouse fact and dimension tables.
- dbt builds analytical marts for the dashboard.
- Looker Studio presents a five-city comparison dashboard.

## Tech Stack

- Cloud platform: GCP
- Infrastructure as code: Terraform
- Orchestration: Airflow
- Ingestion: Python
- Batch transformation: Spark
- Data lake: Google Cloud Storage
- Warehouse: BigQuery
- Analytical modeling: dbt
- Dashboard: Looker Studio
- Environment tooling: `uv`

## Data Flow

The pipeline uses the following main components:

- [ingestion/download_air_quality_data.py](ingestion/download_air_quality_data.py) downloads raw OpenAQ archive files into Bronze.
- [spark/bronze_to_silver.py](spark/bronze_to_silver.py) standardizes Bronze data into Silver parquet.
- [spark/check_silver_data_quality.py](spark/check_silver_data_quality.py) validates the Silver dataset and writes a machine-readable quality report.
- [warehouse/load_to_bigquery.py](warehouse/load_to_bigquery.py) loads Silver outputs into BigQuery.
- [dbt/air_quality_project/models/staging/stg_air_quality.sql](dbt/air_quality_project/models/staging/stg_air_quality.sql) and the reporting marts turn warehouse tables into dashboard-ready outputs.
- [airflow/global_city_air_quality_observatory_dag.py](airflow/global_city_air_quality_observatory_dag.py) orchestrates the end-to-end batch flow.

## Dashboard Story

The dashboard is a five-city comparison dashboard, not a global ranking dashboard.

It is organized around four reviewer-friendly views:

- pollution trend over time by city
- pollutant distribution by city
- cross-city comparison
- extreme pollution events within the five selected cities

Primary dashboard documentation lives in [dashboards/README.md](dashboards/README.md).

## Warehouse Design

The warehouse is designed around a central fact table plus supporting dimensions:

- `fct_air_quality_measurements`
- `dim_city`
- `dim_pollutant`

The fact table is:

- partitioned by `measurement_date`
- clustered by `city` and `pollutant`

That layout matches the dashboard query pattern because users most often filter by date, compare cities, and compare pollutants.

## Reproducibility

The fastest end-to-end local workflow is:

```bash
uv sync
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

Full environment, cloud, and orchestration steps are documented in [runbook.md](runbook.md).

## Lessons Learned

Short retrospective notes live in [docs/lessons-learned.md](docs/lessons-learned.md).

## Architecture Decisions

The main tradeoffs are documented in [docs/architecture-decisions.md](docs/architecture-decisions.md).

## Reviewer Guide

A short reviewer-facing guide lives in [docs/review-guide.md](docs/review-guide.md).

## Proof Of Run

Expected proof-of-run artifacts are listed in [docs/execution-evidence.md](docs/execution-evidence.md).

## Reviewer Checklist

Reviewers should be able to confirm that:

- the README and scope file agree on the same five cities
- Spark is the main Bronze to Silver transformation layer
- Airflow orchestrates the batch pipeline from scope check through dbt validation
- BigQuery stores partitioned and clustered warehouse tables
- dbt produces dashboard-facing marts
- the dashboard tells a five-city comparison story

## Limitations

- Results depend on the selected OpenAQ locations for each city.
- The pipeline is scheduled batch processing, not streaming.
- Source units are preserved from the archive and are not deeply harmonized.
- City-level rollups can hide within-city station variation.
