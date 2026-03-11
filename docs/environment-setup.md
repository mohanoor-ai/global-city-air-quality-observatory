# Environment Setup

## Required tools

- Git
- Python 3.14+
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
