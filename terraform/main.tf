resource "google_storage_bucket" "data_lake" {
  name          = var.gcs_bucket_name
  location      = var.bucket_location
  force_destroy = false
  uniform_bucket_level_access = true
}

resource "google_bigquery_dataset" "warehouse" {
  dataset_id                 = var.bigquery_dataset_id
  location                   = var.bigquery_location
  delete_contents_on_destroy = false
}
