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
  default_partition_expiration_ms = 5184000000
  default_table_expiration_ms     = 5184000000
}

resource "google_bigquery_table" "air_quality_measurements" {
  dataset_id = google_bigquery_dataset.warehouse.dataset_id
  table_id   = var.bigquery_table_id

  schema = <<EOF
[
  {"name": "measurement_datetime", "type": "TIMESTAMP", "mode": "REQUIRED"},
  {"name": "location_name", "type": "STRING", "mode": "REQUIRED"},
  {"name": "latitude", "type": "FLOAT", "mode": "REQUIRED"},
  {"name": "longitude", "type": "FLOAT", "mode": "REQUIRED"},
  {"name": "pollutant", "type": "STRING", "mode": "REQUIRED"},
  {"name": "value", "type": "FLOAT", "mode": "REQUIRED"},
  {"name": "unit", "type": "STRING", "mode": "REQUIRED"}
]
EOF

  time_partitioning {
    type  = "DAY"
    field = "measurement_datetime"
  }
}
