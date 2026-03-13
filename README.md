# Global City Air Quality Observatory

Batch data engineering project comparing air pollution trends and pollutant patterns across London, New York, Delhi, Beijing, and São Paulo using GCP, Airflow, Spark, BigQuery, dbt, and Looker Studio.

## Problem statement

How do pollution trends and pollutant patterns differ across five major global cities over time?

This project compares:

- London
- New York
- Delhi
- Beijing
- São Paulo

## Why this project

Air pollution is a meaningful cross-city comparison problem because the same pollutants can behave differently across places, seasons, and monitoring environments.

This project uses a fixed five-city scope to stay focused, reviewer-friendly, and reproducible. The goal is not global ranking. The goal is a consistent five-city comparison built as an end-to-end batch data engineering project.

## Scope

This project is intentionally limited to these five cities only:

- London
- New York
- Delhi
- Beijing
- São Paulo

The single source of truth for project scope is [ingestion/location_targets.csv](ingestion/location_targets.csv).

## Architecture

```text
OpenAQ source data
-> Bronze ingestion to Google Cloud Storage
-> Spark Bronze to Silver transformation
-> BigQuery warehouse loading
-> dbt analytical marts
-> Looker Studio dashboard
```

Architecture diagram: [images/architecture_diagram.svg](images/architecture_diagram.svg)

## Tech stack

- Google Cloud Platform
- Terraform
- Apache Airflow
- Apache Spark
- Google Cloud Storage
- BigQuery
- dbt
- Looker Studio
- uv

## Pipeline steps

1. download raw OpenAQ archive data for the five configured cities
2. store raw files in Bronze
3. transform raw data to Silver using Spark
4. run Silver data quality checks
5. load curated warehouse data into BigQuery
6. build reporting marts with dbt
7. visualize five-city outputs in Looker Studio

Main execution files:

- [main.py](main.py)
- [ingestion/download_air_quality_data.py](ingestion/download_air_quality_data.py)
- [spark/bronze_to_silver.py](spark/bronze_to_silver.py)
- [spark/check_silver_data_quality.py](spark/check_silver_data_quality.py)
- [warehouse/load_to_bigquery.py](warehouse/load_to_bigquery.py)
- [airflow/global_city_air_quality_observatory_dag.py](airflow/global_city_air_quality_observatory_dag.py)

Spark is the official Bronze to Silver transformation engine in this repository.

## Airflow orchestration

The repo contains Airflow DAGs for:

- backfill runs
- daily runs

The DAG task flow is:

- show_scope
- download_data
- verify_bronze
- bronze_to_silver
- silver_data_quality
- load_bigquery
- dbt_run
- dbt_test
- verify_quality_report

## Warehouse design

- the fact table is partitioned by date using `measurement_date`
- the fact table is clustered by `city` and `pollutant`
- supporting dimensions make reporting and filtering easier
- dbt builds analytical marts from warehouse data for dashboard use

## Dashboard story

The dashboard is a five-city comparison dashboard.

It focuses on:

- city trend over time
- pollutant distribution by city
- cross-city comparison
- extreme pollution events within the five selected cities

Dashboard documentation:

- [dashboards/README.md](dashboards/README.md)

## Reproducibility

For a learner-friendly end-to-end run:

1. install dependencies with `uv`
2. configure environment variables and cloud credentials
3. provision infrastructure with Terraform
4. start Airflow
5. trigger the DAG
6. run dbt if needed
7. inspect BigQuery and dashboard outputs

Useful commands:

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

Full setup and runnable details live in [runbook.md](runbook.md).

## Lessons learned

Keeping the scope fixed to five cities made the project easier to explain, validate, and dashboard cleanly. Spark became the right choice once the Bronze to Silver step needed schema enforcement, metadata enrichment, deduplication, and repeatable parquet output. BigQuery partitioning and clustering mattered because the project constantly filters by date, city, and pollutant.

## Architecture decisions

- [docs/architecture-decisions.md](docs/architecture-decisions.md)

## Reviewer guide

- [docs/review-guide.md](docs/review-guide.md)

## Proof of run

- [docs/execution-evidence.md](docs/execution-evidence.md)
