# Pipeline Overview

This document provides a complete overview of the project pipeline.

It explains how data moves through the system from the source to the final dashboard.

The goal is to make the architecture easy to understand for reviewers, collaborators, and recruiters.

---

# End-to-End Flow

The project follows this flow:

OpenAQ  
→ Python ingestion  
→ Bronze raw csv.gz files  
→ Processing and Silver Parquet output  
→ Data quality gate  
→ Google Cloud Storage (bronze/silver)  
→ BigQuery tables  
→ dbt models  
→ Analytics tables  
→ Looker Studio dashboard  

Airflow orchestrates the workflow across these stages.

---

# Architecture Summary

The project uses a batch-oriented ELT design.

## Source

The source is the OpenAQ air quality dataset.

This provides pollution measurements for pollutants such as:

- PM2.5
- PM10
- NO2
- SO2
- CO
- O3

---

## Ingestion

Python scripts extract the data from OpenAQ.

The ingestion step converts the source response into a structured tabular format and stores it as Parquet.

This keeps the ingestion layer aligned with modern data engineering practices.

---

## Raw Data Lake Layer

The raw layer stores source data with minimal modification.

Storage location example:

```text
gs://air-quality-data-lake/raw/openaq/year=YYYY/month=MM/

This layer acts as the source of truth.

Curated Data Lake Layer

The curated layer stores cleaned and structured Parquet files.

Storage location example:
gs://air-quality-data-lake/curated/air_quality/year=YYYY/month=MM/

This layer is used for warehouse loading.

Data Warehouse

Curated files are loaded into BigQuery.

BigQuery stores the analytical tables used by dbt and the dashboard.

Warehouse examples:

raw measurement tables

fact table for air quality measurements

dimension tables for location and pollutant

Transformation Layer

dbt transforms warehouse data into analytics-ready models.

dbt layers include:

staging

intermediate

marts

These models prepare the final tables for reporting and dashboard use.

Dashboard Layer

The final dashboard is built in Looker Studio.

The dashboard presents key air quality metrics such as:

pollution trends over time

country-level comparisons

city-level comparisons

pollutant distribution

Orchestration

Apache Airflow manages the workflow.

Airflow handles:

scheduling

task order

retries

pipeline monitoring

It ensures the full batch pipeline runs in the correct sequence.

Full Pipeline Sequence

The full sequence of steps is:

extract data from OpenAQ

save Bronze csv.gz files locally

clean and transform the data

save Silver Parquet files

run data quality gate checks

upload Bronze and Silver files to GCS

load data into BigQuery

run dbt models

validate results

update the dashboard

High-Level Diagram
OpenAQ
  ↓
Python Ingestion
  ↓
Bronze csv.gz
  ↓
Processing / Cleaning
  ↓
Silver Parquet
  ↓
Data Quality Gate
  ↓
GCS Bronze/Silver
  ↓
BigQuery
  ↓
dbt
  ↓
Analytics Tables
  ↓
Looker Studio Dashboard

Airflow sits above this process and orchestrates the full workflow.

Why This Design

This design was chosen because it is:

easy to understand

aligned with Zoomcamp conventions

cloud-based

reproducible

scalable

suitable for analytics workflows

It also clearly separates:

ingestion

storage

transformation

visualization

Main Benefits

This pipeline design provides:

clear separation of raw and transformed data

reusable storage in Parquet format

strong compatibility with BigQuery and dbt

simple orchestration with Airflow

an understandable architecture for reviewers

Expected Outcome

When the project is complete, the system will:

ingest air quality data automatically

store data in a structured data lake

transform data in the warehouse

expose metrics through a dashboard

provide useful insights into global air pollution trends
