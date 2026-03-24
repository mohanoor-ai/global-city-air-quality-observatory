# Reviewer Guide

This is the fastest way to inspect the project without running the full
pipeline.

## What The Project Does

A batch pipeline that downloads OpenAQ archive data for five cities, transforms
it to Silver parquet with Spark, stages it in GCS, loads it into BigQuery,
builds dbt marts, and shows the results in Looker Studio.

## 5-Minute File Check

| What to inspect | File |
|---|---|
| Problem statement and run steps | `README.md` |
| Airflow DAG | `airflow/dags/global_city_air_quality_observatory_dag.py` |
| Ingestion | `ingestion/download_air_quality_data.py` |
| City scope | `ingestion/location_targets.csv` |
| Spark transform | `spark/bronze_to_silver.py` |
| Silver DQ | `spark/check_silver_data_quality.py` |
| BigQuery load | `warehouse/load_to_bigquery.py` |
| dbt project | `dbt/air_quality_project/` |
| Terraform | `terraform/main.tf` |
| Proof of run | `docs/execution-evidence.md` |

## What To Verify Quickly

- The project question is a fixed five-city comparison.
- Airflow is the official orchestration path.
- Bronze, Silver, warehouse, dbt, and dashboard steps all exist.
- Terraform provisions the bucket and BigQuery dataset/tables.
- The fact table is partitioned by `measurement_date` and clustered by `city`
  and `pollutant`.
- Dashboard proof and run screenshots are committed in `docs/images/`.

## Reproducibility

The shortest reviewer path is:

1. read `README.md`
2. create a local `.venv` and install `requirements.txt`
3. inspect the DAG and stage scripts
4. check `docs/execution-evidence.md`
5. use `make run` for a manual path or `make airflow-start` for Airflow

Required local config files:

- `.env` copied from `.env.example` for Airflow
- `terraform/terraform.tfvars` copied from `terraform/terraform.tfvars.example`

## Known Limitations

- Cloud steps still require valid GCP credentials.
- Airflow local startup depends on Docker Desktop or Docker Engine being
  accessible from the current shell.
- The dashboard is external to the repo, so the committed screenshot and PDF are
  the fallback evidence.
