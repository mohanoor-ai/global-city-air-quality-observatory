variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "Default GCP region for provider operations"
  type        = string
  default     = "europe-west2"
}

variable "gcs_bucket_name" {
  description = "Name of the data lake GCS bucket"
  type        = string
}

variable "bucket_location" {
  description = "Location/region for GCS bucket"
  type        = string
  default     = "EU"
}

variable "bigquery_dataset_id" {
  description = "BigQuery dataset ID for warehouse tables"
  type        = string
  default     = "air_quality_dw"
}

variable "bigquery_location" {
  description = "BigQuery dataset location"
  type        = string
  default     = "EU"
}

variable "bigquery_table_id" {
  description = "BigQuery table ID for cleaned air quality measurements"
  type        = string
  default     = "air_quality_measurements"
}
