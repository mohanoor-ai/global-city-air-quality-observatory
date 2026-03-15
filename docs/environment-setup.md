# Environment Setup

## Required tools

- Git
- Python 3.11 to 3.13
- `uv` for the development workflow, or `pip` with `requirements.txt` for reviewer setup
- Google Cloud SDK (`gcloud`, `bq`)
- Terraform (only if you want to provision cloud resources)
- Airflow (only if you want to run DAGs locally)

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

For reviewer-friendly installation without `uv`:

```bash
python -m venv .venv-review
source .venv-review/bin/activate
python -m pip install -r requirements.txt
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
