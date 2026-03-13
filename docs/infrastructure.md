# Infrastructure Notes

Terraform now provisions the main rubric-relevant cloud resources:

- one GCS data lake bucket
- `bronze/` and `silver/` storage prefixes
- one BigQuery dataset
- one partitioned and clustered fact table: `fct_air_quality_measurements`
- two helper dimensions: `dim_city` and `dim_pollutant`

Files:

- `terraform/main.tf`
- `terraform/variables.tf`
- `terraform/outputs.tf`
- `terraform/versions.tf`

Manual work still required:

- creating the GCP project
- configuring authentication
- running the pipeline jobs that populate Bronze, Silver, and warehouse tables
