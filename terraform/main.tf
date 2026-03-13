resource "google_storage_bucket" "data_lake" {
  name                        = var.gcs_bucket_name
  location                    = var.bucket_location
  force_destroy               = false
  uniform_bucket_level_access = true
}

resource "google_storage_bucket_object" "bronze_prefix" {
  name    = "bronze/.keep"
  bucket  = google_storage_bucket.data_lake.name
  content = "bronze landing zone"
}

resource "google_storage_bucket_object" "silver_prefix" {
  name    = "silver/.keep"
  bucket  = google_storage_bucket.data_lake.name
  content = "silver parquet landing zone"
}

resource "google_bigquery_dataset" "warehouse" {
  dataset_id                 = var.bigquery_dataset_id
  location                   = var.bigquery_location
  delete_contents_on_destroy = false
}

resource "google_bigquery_table" "fct_air_quality_measurements" {
  dataset_id = google_bigquery_dataset.warehouse.dataset_id
  table_id   = var.fact_table_id

  schema = <<EOF
[
  {"name": "city", "type": "STRING", "mode": "REQUIRED"},
  {"name": "country", "type": "STRING", "mode": "REQUIRED"},
  {"name": "location_id", "type": "INT64", "mode": "REQUIRED"},
  {"name": "location_name", "type": "STRING", "mode": "NULLABLE"},
  {"name": "sensor_id", "type": "INT64", "mode": "NULLABLE"},
  {"name": "pollutant", "type": "STRING", "mode": "REQUIRED"},
  {"name": "measurement_value", "type": "FLOAT64", "mode": "REQUIRED"},
  {"name": "measurement_unit", "type": "STRING", "mode": "NULLABLE"},
  {"name": "measurement_datetime", "type": "TIMESTAMP", "mode": "REQUIRED"},
  {"name": "measurement_date", "type": "DATE", "mode": "REQUIRED"},
  {"name": "latitude", "type": "FLOAT64", "mode": "NULLABLE"},
  {"name": "longitude", "type": "FLOAT64", "mode": "NULLABLE"},
  {"name": "batch_date", "type": "DATE", "mode": "NULLABLE"},
  {"name": "source_file", "type": "STRING", "mode": "NULLABLE"}
]
EOF

  time_partitioning {
    type  = "DAY"
    field = "measurement_date"
  }

  clustering = ["city", "pollutant"]
}

resource "google_bigquery_table" "dim_city" {
  dataset_id = google_bigquery_dataset.warehouse.dataset_id
  table_id   = var.city_dim_table_id

  schema = <<EOF
[
  {"name": "city", "type": "STRING", "mode": "REQUIRED"},
  {"name": "country", "type": "STRING", "mode": "REQUIRED"},
  {"name": "station_count", "type": "INT64", "mode": "NULLABLE"},
  {"name": "avg_latitude", "type": "FLOAT64", "mode": "NULLABLE"},
  {"name": "avg_longitude", "type": "FLOAT64", "mode": "NULLABLE"}
]
EOF
}

resource "google_bigquery_table" "dim_pollutant" {
  dataset_id = google_bigquery_dataset.warehouse.dataset_id
  table_id   = var.pollutant_dim_table_id

  schema = <<EOF
[
  {"name": "pollutant", "type": "STRING", "mode": "REQUIRED"},
  {"name": "measurement_unit", "type": "STRING", "mode": "NULLABLE"}
]
EOF
}
