output "data_lake_bucket_name" {
  description = "Provisioned GCS bucket for the data lake"
  value       = google_storage_bucket.data_lake.name
}

output "bigquery_dataset_id" {
  description = "Provisioned BigQuery dataset ID"
  value       = google_bigquery_dataset.warehouse.dataset_id
}

output "bigquery_table_id" {
  description = "Provisioned BigQuery table ID"
  value       = google_bigquery_table.air_quality_measurements.table_id
}
