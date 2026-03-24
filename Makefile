.PHONY: setup infra infra-destroy run run-ingest run-transform run-load run-dbt airflow-start test clean

setup:
	uv sync
	@echo "Python dependencies installed"

infra:
	cd terraform && terraform init && terraform apply -var-file=terraform.tfvars -auto-approve
	@echo "GCP resources provisioned"

infra-destroy:
	cd terraform && terraform destroy -var-file=terraform.tfvars -auto-approve

run: run-ingest run-transform run-load run-dbt

run-ingest:
	uv run python main.py show-scope
	uv run python ingestion/download_air_quality_data.py --mode backfill
	uv run python main.py verify-bronze

run-transform:
	uv run python spark/bronze_to_silver.py --write-mode overwrite
	uv run python spark/check_silver_data_quality.py

run-load:
	uv run python warehouse/load_to_bigquery.py

run-dbt:
	bash scripts/dbt_run.sh
	bash scripts/dbt_test.sh
	uv run python main.py verify-quality-report

airflow-start:
	uv venv .venv-airflow --python 3.11
	.venv-airflow/bin/python -m pip install apache-airflow
	PATH="$(CURDIR)/.venv-airflow/bin:$$PATH" bash scripts/airflow_standalone.sh

test:
	uv run python -m unittest -v tests/test_pipeline_checks.py

clean:
	rm -rf data/bronze/* data/silver/* data/quality/*
	@echo "Local data layers cleared"
