# Project Plan

## Status Summary

Current phase: **Phase 4 — Data Quality Gate**  
Overall state: **work in progress**

---

## Phase 1 — Project Foundation

Status: mostly done

- [x] create GitHub repository
- [x] define repository structure
- [x] create documentation folder
- [x] write project README
- [x] define pipeline architecture
- [x] define dashboard goals
- [x] define pollutants used
- [x] define medallion architecture
- [x] create Python environment with `uv`
- [x] configure base dependencies
- [x] configure development environment

## Phase 2 — Data Ingestion (Bronze Layer)

Status: working

- [x] identify OpenAQ AWS archive
- [x] understand dataset structure
- [x] confirm pollutant names
- [x] implement `ingestion/download_air_quality_data.py`
- [x] connect to AWS S3 with `boto3`
- [x] list archive files
- [x] download raw files
- [x] store raw files in `data/bronze/`
- [x] keep Bronze format as `.csv.gz`

## Phase 3 — Data Processing (Silver Layer)

Status: implemented (local pipeline)

- [x] create `processing/clean_air_quality_data.py`
- [x] read all Bronze `.csv.gz` files
- [x] combine files into one dataset
- [x] filter pollutants: `pm25`, `pm10`, `no2`, `co`, `o3`
- [x] rename columns
- [x] convert datetime columns
- [x] validate schema
- [x] write `data/silver/air_quality_location-<id>_<startdate>_<enddate>.parquet`

## Phase 4 — Data Quality Gate

Status: in progress (quality gate before warehouse)

- [x] run Silver dataset quality checks
- [x] check row counts
- [ ] verify pollutant distribution
- [x] verify timestamps
- [x] check missing values
- [x] inspect schema
- [x] validate unique pollutants, date range, and min/max values

## Phase 5 — Cloud Infrastructure

Status: planned

- [ ] create GCP project
- [ ] create service account
- [ ] configure credentials
- [ ] provision GCS bucket via Terraform
- [ ] provision BigQuery dataset via Terraform

## Phase 6 — Data Lake Storage

Status: planned

- [ ] upload Bronze data from local to GCS
- [ ] upload Silver Parquet data to GCS
- [ ] enforce storage layout under `gcs://air-quality-data-lake/`
- [ ] use `bronze/` and `silver/` prefixes

## Phase 7 — Data Warehouse (BigQuery)

Status: planned

- [ ] create dataset
- [ ] create `air_quality_measurements` table
- [ ] load parquet files
- [ ] validate table schema:
- [ ] `measurement_datetime`
- [ ] `location_name`
- [ ] `latitude`
- [ ] `longitude`
- [ ] `pollutant`
- [ ] `value`
- [ ] `unit`

## Phase 8 — dbt Modeling

Status: planned

- [ ] create `dbt/air_quality_project`
- [ ] configure BigQuery connection
- [ ] build staging model `stg_air_quality`
- [ ] standardize columns and enforce types
- [ ] build intermediate model `int_pollution_daily`
- [ ] aggregate by day and city
- [ ] build marts:
- [ ] `mart_pollution_by_city`
- [ ] `mart_pollution_by_country`
- [ ] `mart_pollution_trends`

## Phase 9 — Dashboard

Status: planned

- [ ] build Looker Studio dashboard
- [ ] global trend section (PM2.5 over time)
- [ ] polluted cities section
- [ ] polluted countries section
- [ ] pollutant comparison section

## Phase 10 — Orchestration

Status: planned

- [ ] create Airflow DAG `air_quality_pipeline_dag.py`
- [ ] orchestrate ingestion
- [ ] orchestrate processing
- [ ] orchestrate upload
- [ ] orchestrate warehouse load
- [ ] orchestrate `dbt run`

## Phase 11 — Testing

Status: planned

- [ ] test ingestion
- [ ] test processing
- [ ] test warehouse loading
- [ ] validate dbt models

## Phase 12 — Documentation

Status: in progress

- [ ] keep README updated
- [ ] write pipeline overview
- [ ] write architecture decisions
- [ ] document dataset
- [ ] document dashboard metrics

## Phase 13 — Final Polishing

Status: planned

- [ ] optimize ingestion script
- [ ] optimize Silver dataset
- [ ] improve code structure
- [ ] clean repository
- [ ] add dashboard screenshots
- [ ] prepare portfolio presentation

---

## Final Target Pipeline

OpenAQ AWS  
↓  
Python ingestion  
↓  
Bronze layer (`csv.gz`)  
↓  
Processing script  
↓  
Silver layer (Parquet)  
↓  
Data quality gate  
↓  
Google Cloud Storage  
↓  
BigQuery  
↓  
dbt models  
↓  
Analytics marts  
↓  
Looker Studio dashboard
