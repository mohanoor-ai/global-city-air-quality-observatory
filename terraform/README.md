# Terraform - GCP infrastructure

This directory provisions the storage and warehouse resources used by the
pipeline. The configuration is intentionally small and maps directly to the
Bronze, Silver, and BigQuery stages described in the project README.

---

## Resources created

| Resource | Type | Terraform name |
|---|---|---|
| Data lake bucket | `google_storage_bucket` | `data_lake` |
| Bronze prefix placeholder | `google_storage_bucket_object` | `bronze_prefix` |
| Silver prefix placeholder | `google_storage_bucket_object` | `silver_prefix` |
| BigQuery dataset | `google_bigquery_dataset` | `warehouse` |
| Fact table | `google_bigquery_table` | `fct_air_quality_measurements` |
| City dimension | `google_bigquery_table` | `dim_city` |
| Pollutant dimension | `google_bigquery_table` | `dim_pollutant` |

The fact table is partitioned by `measurement_date` and clustered by `city` and
`pollutant`.

---

## Key resource blocks

```hcl
resource "google_storage_bucket" "data_lake" {
  name                        = var.gcs_bucket_name
  location                    = var.bucket_location
  force_destroy               = false
  uniform_bucket_level_access = true
}

resource "google_bigquery_dataset" "warehouse" {
  dataset_id                 = var.bigquery_dataset_id
  location                   = var.bigquery_location
  delete_contents_on_destroy = false
}

resource "google_bigquery_table" "fct_air_quality_measurements" {
  dataset_id = google_bigquery_dataset.warehouse.dataset_id
  table_id   = var.fact_table_id

  time_partitioning {
    type  = "DAY"
    field = "measurement_date"
  }

  clustering = ["city", "pollutant"]
}
```

---

## Variables

| Variable | Description | Example |
|---|---|---|
| `project_id` | GCP project ID | `my-gcp-project` |
| `region` | Default provider region | `europe-west2` |
| `gcs_bucket_name` | Data lake bucket name | `global-city-air-quality-observatory-yourname` |
| `bucket_location` | Bucket storage location | `EU` |
| `bigquery_dataset_id` | Warehouse dataset ID | `air_quality_dw` |
| `bigquery_location` | BigQuery dataset location | `EU` |
| `fact_table_id` | Warehouse fact table ID | `fct_air_quality_measurements` |
| `city_dim_table_id` | City dimension table ID | `dim_city` |
| `pollutant_dim_table_id` | Pollutant dimension table ID | `dim_pollutant` |

Copy the committed template before planning or applying:

```bash
cp terraform/terraform.tfvars.example terraform/terraform.tfvars
```

Then edit `terraform/terraform.tfvars` with your real project values.

---

## Commands

```bash
cd terraform
terraform init
terraform plan -var-file=terraform.tfvars
terraform apply -var-file=terraform.tfvars
terraform destroy -var-file=terraform.tfvars
```

---

## Outputs

Terraform also exposes these outputs from `outputs.tf`:

- `data_lake_bucket_name`
- `bigquery_dataset_id`
- `warehouse_fact_table_id`
- `warehouse_city_dim_table_id`
- `warehouse_pollutant_dim_table_id`
