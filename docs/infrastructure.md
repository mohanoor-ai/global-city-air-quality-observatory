# Infrastructure Notes

This project keeps infrastructure intentionally small.

## What Terraform creates

From `terraform/`, this repo provisions:

- one GCS bucket (data lake bucket)
- one BigQuery dataset (`air_quality_dw` by default)
- one BigQuery table (`air_quality_measurements` by default)

Files:

- `terraform/main.tf`
- `terraform/variables.tf`
- `terraform/outputs.tf`
- `terraform/versions.tf`

## What is still manual

- creating the GCP project
- creating and configuring service account credentials
- local auth setup for `gcloud` / `bq`
- running warehouse load and dbt commands

## Scope decision

This scope is intentionally minimal:

- minimal cloud resources
- easy to explain in project review
- avoids extra services that are not required for the core PM2.5 analysis story
