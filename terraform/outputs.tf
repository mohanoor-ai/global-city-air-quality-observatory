output "data_lake_bucket_name" {
  description = "Provisioned GCS bucket for the data lake"
  value       = google_storage_bucket.data_lake.name
}

output "bigquery_dataset_id" {
  description = "Provisioned BigQuery dataset ID"
  value       = google_bigquery_dataset.warehouse.dataset_id
}

output "warehouse_fact_table_id" {
  description = "Provisioned BigQuery fact table ID"
  value       = google_bigquery_table.fct_air_quality_measurements.table_id
}

output "warehouse_city_dim_table_id" {
  description = "Provisioned BigQuery city dimension table ID"
  value       = google_bigquery_table.dim_city.table_id
}

output "warehouse_pollutant_dim_table_id" {
  description = "Provisioned BigQuery pollutant dimension table ID"
  value       = google_bigquery_table.dim_pollutant.table_id
}
