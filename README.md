
# Air Quality Data Pipeline

**Data Engineering Zoomcamp Final Project**

An end-to-end **data engineering pipeline** that ingests global air quality measurements, processes them into analytics-ready datasets, and visualizes pollution trends through an interactive dashboard.

This project demonstrates modern **data lake, data warehouse, orchestration, and analytics engineering practices** using industry-standard tools.

---

# Project Overview

Air pollution is one of the most significant environmental health risks worldwide. However, raw air quality data is often fragmented across monitoring stations and difficult to analyze without structured pipelines.

This project builds a **scalable batch data pipeline** that:

* ingests global air quality measurements
* stores them in a structured data lake
* transforms the data into analytics-ready tables
* powers dashboards that highlight pollution trends

The project is built as the **final project for the DataTalksClub Data Engineering Zoomcamp**.

---

# Project Goals

The pipeline demonstrates:

* dataset ingestion
* data lake architecture
* batch pipeline design
* data warehouse modeling
* dbt transformations
* workflow orchestration
* infrastructure as code
* analytics dashboards

The project is designed as a **portfolio-quality data engineering pipeline** suitable for technical review by recruiters and hiring managers.

---

# Primary Business Question

**Which countries and cities experience the highest PM2.5 exposure over time, and how are pollution trends changing across regions and pollutants?**

---

# Dashboard Story

Instead of displaying many unrelated charts, the dashboard focuses on a small number of clear insights.

### Global Pollution Trend

How pollution levels change over time.

### Most Polluted Countries

Countries with the highest average pollution exposure.

### Most Polluted Cities

Cities with the highest pollutant concentrations.

### Pollutant Comparison

How different pollutants vary across regions and time.

This structure allows users to quickly identify pollution hotspots and trends.

---

# Key Dashboard Metrics

The pipeline produces the following metrics used in the dashboard.

### Exposure Metrics

Average PM2.5 by country
Average PM10 by city

### Peak Pollution Metrics

Highest recorded pollutant value by location

### Trend Metrics

Monthly pollution trend by pollutant

### Distribution Metrics

Pollutant distribution across countries and cities

---

# Architecture

The pipeline follows a **batch ELT architecture**.

```
OpenAQ Dataset (AWS)
        ↓
Python ingestion
        ↓
Bronze Data Lake Layer (raw parquet)
        ↓
Silver Layer (cleaned data)
        ↓
BigQuery Data Warehouse
        ↓
dbt Transformations
        ↓
Gold Analytics Mart Tables
        ↓
Looker Studio Dashboard
```

Pipeline orchestration is handled by **Apache Airflow**.
Infrastructure is provisioned using **Terraform**.

---

# Technology Stack

| Layer           | Technology           |
| --------------- | -------------------- |
| Ingestion       | Python               |
| Processing      | Pandas, PyArrow      |
| Storage         | Parquet              |
| Data Lake       | Google Cloud Storage |
| Warehouse       | BigQuery             |
| Transformations | dbt                  |
| Orchestration   | Apache Airflow       |
| Infrastructure  | Terraform            |
| Visualization   | Looker Studio        |
| Environment     | uv                   |

---

# Data Source

The project uses the **OpenAQ global air quality dataset**.

OpenAQ aggregates pollution measurements from monitoring stations worldwide.

Website
[https://openaq.org](https://openaq.org)

GitHub
[https://github.com/openaq](https://github.com/openaq)

Initial ingestion uses the **OpenAQ dataset hosted on AWS**.

---

# Pollutants Included

The analysis focuses on several widely monitored air pollutants.

| Pollutant | Description                                             |
| --------- | ------------------------------------------------------- |
| PM2.5     | Fine particulate matter smaller than 2.5µm              |
| PM10      | Coarse particulate matter smaller than 10µm             |
| NO₂       | Nitrogen dioxide mainly from traffic emissions          |
| CO        | Carbon monoxide from incomplete combustion              |
| O₃        | Ground-level ozone formed through atmospheric reactions |

These pollutants are commonly used to measure **air pollution exposure and environmental health risks**.

---

# Data Lake Design

The pipeline follows a **Medallion Architecture**.

### Bronze Layer

Raw ingestion data stored as partitioned parquet files.

### Silver Layer

Cleaned and standardized measurements.

### Gold Layer

Analytics-ready tables used by dashboards.

---

# Data Mart Tables

To support the dashboard metrics, the pipeline generates several **analytics mart tables**.

### mart_pollution_by_country

Aggregated pollution metrics by country.

Example fields

```
country
pollutant
avg_value
max_value
measurement_count
month
```

---

### mart_pollution_by_city

City-level pollution exposure.

```
city
country
pollutant
avg_value
max_value
month
```

---

### mart_pollution_trends

Time-series pollution trends.

```
date
pollutant
avg_value
measurement_count
```

---

### mart_pollutant_distribution

Distribution of pollutants across locations.

```
country
city
pollutant
value
timestamp
```

---

# Repository Structure

```
air-quality-data-pipeline

├── ingestion
│   └── download_air_quality_data.py
│
├── processing
│   └── clean_air_quality_data.py
│
├── airflow
│   └── dags
│
├── dbt
│   └── air_quality_project
│
├── data
│   ├── bronze
│   ├── silver
│   └── gold
│
├── docs
│   ├── README.md
│   ├── project-plan.md
│   ├── architecture-decisions.md
│   ├── pipeline-overview.md
│   ├── pipeline-orchestration.md
│   ├── repository-structure.md
│   ├── analytics-and-metrics.md
│   ├── data-source.md
│   ├── data-lake-design.md
│   ├── environment-setup.md
│   └── local-setup.md
│
├── terraform
│
├── tests
│
└── README.md
```

---

# Setup

## Prerequisites

Python 3.10+
Docker
Google Cloud account
dbt
Terraform

---

## Clone Repository

```
git clone https://github.com/mohanoor-ai/air-quality-data-pipeline.git
cd air-quality-data-pipeline
```

---

## Install Dependencies

```
uv pip install -r requirements.txt
```

---

## Environment Variables

```
export OPENAQ_API_KEY="your_api_key"
```

---

# Running the Pipeline

### 1 Ingest Data

```
python ingestion/download_air_quality_data.py
```

Downloads raw measurements into the Bronze layer.

---

### 2 Clean Data

```
python processing/clean_air_quality_data.py
```

Produces the Silver dataset.

---

### 3 Load Data to BigQuery

```
python processing/load_to_bigquery.py
```

---

### 4 Run dbt Transformations

```
cd dbt/air_quality_project
dbt run
```

---

### 5 Run Airflow

```
airflow scheduler
airflow webserver
```

Airflow orchestrates the entire pipeline.

---

# Testing

Run tests using:

```
pytest tests/
```

Tests validate:

* schema correctness
* ingestion logic
* transformation outputs

---

# Security

API keys and credentials should **never be committed to GitHub**.

Use environment variables for authentication.

---

# Future Improvements

Possible future enhancements include:

* streaming ingestion pipeline
* automated data quality checks
* CI/CD deployment
* geospatial pollution analysis
* anomaly detection for pollution spikes
* historical dataset backfills

---

# What This Project Demonstrates

This project demonstrates practical data engineering skills including:

* batch pipeline architecture
* data lake design
* warehouse modeling
* dbt transformations
* Airflow orchestration
* infrastructure as code
* analytics dashboard design

---
