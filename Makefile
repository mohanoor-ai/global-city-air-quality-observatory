.PHONY: setup infra run airflow-init airflow-start airflow-stop test clean

setup:
	python -m venv .venv
	.venv/bin/pip install -r requirements.txt
	@echo "Dependencies installed in .venv"

infra:
	cd terraform && terraform init
	cd terraform && terraform apply -var-file=terraform.tfvars -auto-approve
	@echo "Terraform apply complete"

run:
	.venv/bin/python ingestion/download_air_quality_data.py --validate-scope
	.venv/bin/python ingestion/download_air_quality_data.py --mode backfill
	.venv/bin/python ingestion/download_air_quality_data.py --verify-bronze
	.venv/bin/python spark/bronze_to_silver.py --write-mode overwrite
	.venv/bin/python spark/check_silver_data_quality.py
	.venv/bin/python warehouse/load_to_bigquery.py
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

airflow-init:
	@docker compose version >/dev/null 2>&1 || { \
		echo "Docker Compose is not accessible from this shell."; \
		echo "If you are using WSL, enable Docker Desktop WSL integration for this distro."; \
		exit 1; \
	}
	@if [ ! -f .env ] && [ -f .env.example ]; then cp .env.example .env; fi
	docker compose up airflow-init

airflow-start:
	@docker compose version >/dev/null 2>&1 || { \
		echo "Docker Compose is not accessible from this shell."; \
		echo "If you are using WSL, enable Docker Desktop WSL integration for this distro."; \
		exit 1; \
	}
	docker compose up -d
	@echo "Airflow UI available at http://localhost:8080"

airflow-stop:
	@docker compose version >/dev/null 2>&1 || { \
		echo "Docker Compose is not accessible from this shell."; \
		echo "If you are using WSL, enable Docker Desktop WSL integration for this distro."; \
		exit 1; \
	}
	docker compose down

test:
	.venv/bin/python -m unittest -v tests/test_pipeline_checks.py

clean:
	rm -rf data/bronze/* data/silver/* data/quality/*
	@echo "Local data layers cleared"
