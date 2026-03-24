# Environment Setup

## Required tools

- Git
- Python 3.11 to 3.13
- `uv` for the development workflow, or `pip` with `requirements.txt` as an optional installation path
- Google Cloud SDK (`gcloud`, `bq`)
- Terraform (only if you want to provision cloud resources)
- Docker and Docker Compose (only if you want to run Airflow locally)

## Quick checks

```bash
git --version
python3 --version
# Optional for the development workflow:
uv --version
gcloud --version
bq version
terraform --version
```

## Install Python dependencies

For development:

```bash
uv sync
```

This installs the main project dependencies and dbt into the same local Python
environment.

If you prefer not to use `uv`:

```bash
python -m venv .venv-pip
source .venv-pip/bin/activate
python -m pip install -r requirements.txt
```

## Runtime model

- One local Python environment is used for ingestion, Spark helpers, warehouse
  loading, and dbt
- Docker Compose is used only for local Airflow orchestration

## GCP authentication (recommended)

Authenticate once:

```bash
gcloud auth login
gcloud auth application-default login
```

Then run:

```bash
bash scripts/dbt_run.sh
bash scripts/dbt_test.sh
```

If you run Airflow from WSL with Docker Desktop, make sure WSL integration is
enabled for this distro before using the Docker Compose targets.
