.PHONY: setup infra infra-destroy run run-ingest run-transform run-load run-dbt check-docker airflow-init airflow-start airflow-stop airflow-logs test clean

setup:
	uv sync
	@echo "Python and dbt dependencies installed"

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
	uv run python -m unittest -v tests/test_pipeline_checks.py

clean:
	rm -rf data/bronze/* data/silver/* data/quality/*
	@echo "Local data layers cleared"
