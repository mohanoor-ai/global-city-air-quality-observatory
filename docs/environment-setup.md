# Environment Setup

## Required tools

- Git
- Python 3.11 to 3.13
- `uv`
- Google Cloud SDK (`gcloud`, `bq`)
- Terraform (only if you want to provision cloud resources)
- Airflow (only if you want to run DAGs locally)

## Quick checks

```bash
git --version
python3 --version
uv --version
gcloud --version
bq version
terraform --version
```

## Install Python dependencies

```bash
uv sync
```

## dbt environment

This repo uses a separate dbt virtual environment at `.venv-dbt` for dbt commands.

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
