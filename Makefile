.PHONY: setup infra infra-destroy run run-ingest run-transform run-load run-dbt check-docker airflow-init airflow-start airflow-stop airflow-logs test clean

setup:
	python -m venv .venv
	.venv/bin/pip install -r requirements.txt
	@echo "Python and dbt dependencies installed in .venv"

infra:
	cd terraform && terraform init && terraform apply -var-file=terraform.tfvars -auto-approve
	@echo "GCP resources provisioned"

infra-destroy:
	cd terraform && terraform destroy -var-file=terraform.tfvars -auto-approve

run: run-ingest run-transform run-load run-dbt

run-ingest:
	.venv/bin/python ingestion/download_air_quality_data.py --show-scope
	.venv/bin/python ingestion/download_air_quality_data.py --mode backfill
	.venv/bin/python ingestion/download_air_quality_data.py --verify-bronze

run-transform:
	.venv/bin/python spark/bronze_to_silver.py --write-mode overwrite
	.venv/bin/python spark/check_silver_data_quality.py

run-load:
	.venv/bin/python warehouse/load_to_bigquery.py

run-dbt:
	cd dbt/air_quality_project && \
	DBT_PROFILES_DIR=$$(pwd) \
	PROJECT_ID=$${PROJECT_ID:-$$(sed -n 's/^project_id[[:space:]]*=[[:space:]]*"\(.*\)"/\1/p' ../../terraform/terraform.tfvars | head -n 1)} \
	BIGQUERY_LOCATION=$${BIGQUERY_LOCATION:-$$(sed -n 's/^bigquery_location[[:space:]]*=[[:space:]]*"\(.*\)"/\1/p' ../../terraform/terraform.tfvars | head -n 1)} \
	DBT_DATASET=$${DBT_DATASET:-air_quality_dbt} \
	../../.venv/bin/dbt run --project-dir . --profiles-dir .
	cd dbt/air_quality_project && \
	DBT_PROFILES_DIR=$$(pwd) \
	PROJECT_ID=$${PROJECT_ID:-$$(sed -n 's/^project_id[[:space:]]*=[[:space:]]*"\(.*\)"/\1/p' ../../terraform/terraform.tfvars | head -n 1)} \
	BIGQUERY_LOCATION=$${BIGQUERY_LOCATION:-$$(sed -n 's/^bigquery_location[[:space:]]*=[[:space:]]*"\(.*\)"/\1/p' ../../terraform/terraform.tfvars | head -n 1)} \
	DBT_DATASET=$${DBT_DATASET:-air_quality_dbt} \
	../../.venv/bin/dbt test --project-dir . --profiles-dir .
	.venv/bin/python spark/check_silver_data_quality.py --verify-report

check-docker:
	@docker compose version >/dev/null 2>&1 || { \
		echo "Docker Compose is not accessible from this shell."; \
		echo "If you are using WSL, enable Docker Desktop WSL integration for this distro."; \
		exit 1; \
	}

airflow-init: check-docker
	@if [ ! -f .env ] && [ -f .env.example ]; then cp .env.example .env; fi
	@grep -q '^AIRFLOW_UID=' .env 2>/dev/null || echo "AIRFLOW_UID=$$(id -u)" >> .env
	docker compose up airflow-init

airflow-start: check-docker
	docker compose up -d
	@echo "Airflow UI available at http://localhost:8080"

airflow-stop: check-docker
	docker compose down

airflow-logs: check-docker
	docker compose logs -f airflow-apiserver

test:
	.venv/bin/python -m unittest -v tests/test_pipeline_checks.py

clean:
	rm -rf data/bronze/* data/silver/* data/quality/*
	@echo "Local data layers cleared"
