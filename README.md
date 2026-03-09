# Air Quality Data Pipeline

**Data Engineering Zoomcamp Final Project**

An end-to-end **data engineering pipeline** that ingests global air quality measurements, processes them into analytics-ready datasets, and visualizes pollution trends through a dashboard.

This project demonstrates modern **data lake architecture, data transformation, and analytics engineering practices** using industry-standard tools.

---

# Project Overview

Air pollution is one of the most significant environmental health risks worldwide. However, raw air quality data is often fragmented across monitoring stations and difficult to analyze without structured pipelines.

This project builds a **batch data pipeline** that:

* ingests air quality measurements
* stores raw data in a data lake
* cleans and standardizes the dataset
* transforms it into analytics-ready tables
* powers dashboards that highlight pollution trends

The project is built as the **final project for the DataTalksClub Data Engineering Zoomcamp**.

---

# Project Goals

The pipeline demonstrates practical data engineering concepts:

* bulk dataset ingestion
* data lake architecture
* medallion data model (Bronze / Silver / Gold)
* data cleaning and transformation
* data warehouse modeling
* dbt analytics models
* pipeline orchestration
* dashboard analytics

The project is designed as a **portfolio-quality data engineering pipeline**.

---

# Primary Business Question

**Which countries and cities experience the highest PM2.5 exposure over time, and how are pollution trends changing across regions and pollutants?**

---

# Dashboard Story

The dashboard is structured around a small set of insights rather than many unrelated charts.

### Global Pollution Trends

How air pollution levels change over time.

### Most Polluted Cities

Cities with the highest average pollutant concentrations.

### Most Polluted Countries

Countries with the highest exposure levels.

### Pollutant Comparison

Comparison of different pollutant types across locations.

---

# Key Dashboard Metrics

The pipeline produces several core metrics.

### Exposure Metrics

* Average PM2.5 by country
* Average PM10 by city

### Peak Pollution Metrics

* Highest recorded pollutant value by location

### Trend Metrics

* Monthly pollution trends

### Distribution Metrics

* Distribution of pollutants across locations

---

# Architecture

The pipeline follows a **batch ELT architecture**.

```
OpenAQ AWS Archive
        ↓
Python ingestion
        ↓
Bronze Data Lake Layer (raw csv.gz files)
        ↓
Silver Layer (cleaned parquet dataset)
        ↓
Data Warehouse (BigQuery)
        ↓
dbt Transformations
        ↓
Gold Analytics Mart Tables
        ↓
Looker Studio Dashboard
```

Pipeline orchestration will later be handled by **Apache Airflow**.

Infrastructure provisioning will use **Terraform**.

---

# Technology Stack

| Layer           | Technology                           |
| --------------- | ------------------------------------ |
| Ingestion       | Python                               |
| Processing      | Pandas                               |
| Storage         | CSV / Parquet                        |
| Data Lake       | Local storage → Google Cloud Storage |
| Warehouse       | BigQuery                             |
| Transformations | dbt                                  |
| Orchestration   | Apache Airflow                       |
| Infrastructure  | Terraform                            |
| Visualization   | Looker Studio                        |
| Environment     | uv                                   |

---

# Data Source

The project uses the **OpenAQ archive hosted on AWS Open Data**.

Dataset page:

[https://registry.opendata.aws/openaq/](https://registry.opendata.aws/openaq/)

OpenAQ documentation:

[https://docs.openaq.org/aws/about](https://docs.openaq.org/aws/about)

AWS bucket:

```
s3://openaq-data-archive/
```

---

## Archive Structure

The OpenAQ archive stores data as **daily compressed CSV files** using a partitioned structure:

```
records/csv.gz/locationid={locationid}/year={year}/month={month}/
```

Example file:

```
records/csv.gz/locationid=2178/year=2020/month=12/location-2178-20201231.csv.gz
```

Each file contains measurements for a specific monitoring station for a single day.

---

# Pollutants Included

The analysis focuses on several widely monitored pollutants.

| Pollutant | Description                                             |
| --------- | ------------------------------------------------------- |
| PM2.5     | Fine particulate matter smaller than 2.5µm              |
| PM10      | Coarse particulate matter smaller than 10µm             |
| NO₂       | Nitrogen dioxide mainly from traffic emissions          |
| CO        | Carbon monoxide from incomplete combustion              |
| O₃        | Ground-level ozone formed through atmospheric reactions |

These pollutants are widely used to measure **air pollution exposure and health risk**.

---

# Data Lake Design

The pipeline follows a **Medallion Architecture**.

---

## Bronze Layer

Raw data is stored exactly as downloaded from the OpenAQ archive.

Files remain in their original format:

```
csv.gz
```

Example layout:

```
data/bronze/london/locationid=2178/year=2020/month=01/location-2178-20200101.csv.gz
```

The Bronze layer preserves the **original source data**.

---

## Silver Layer

The Silver layer will contain **cleaned and standardized data**.

Processing steps include:

* reading raw `csv.gz` files
* merging daily datasets
* filtering selected pollutants
* standardizing column names
* converting timestamps
* writing analytics-friendly **Parquet files**

Example output:

```
data/silver/air_quality_2020.parquet
```

---

## Gold Layer

Gold tables will contain **analytics-ready datasets** used by dashboards.

These tables will be built using **dbt models**.

---

# Data Mart Tables

The pipeline will produce several analytics tables.

### mart_pollution_by_country

Aggregated pollution metrics by country.

Example fields:

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
│   ├── project-plan.md
│   ├── architecture-decisions.md
│   ├── pipeline-overview.md
│   ├── analytics-and-metrics.md
│   ├── data-source.md
│   ├── data-lake-design.md
│   └── environment-setup.md
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

* Python 3.10+
* Docker
* Google Cloud account
* dbt
* Terraform

---

## Clone Repository

```
git clone https://github.com/mohanoor-ai/air-quality-data-pipeline.git
cd air-quality-data-pipeline
```

---

## Install Dependencies

Using **uv**:

```
uv pip install -r requirements.txt
```

---

# Running the Pipeline

### 1 Ingest Data

```
python ingestion/download_air_quality_data.py
```

This downloads **one full year of London monitoring data** from the OpenAQ AWS archive into the Bronze layer.

Example storage location:

```
data/bronze/london/locationid=2178/year=2020/month=MM/
```

---

### 2 Clean Data (Next Step)

```
python processing/clean_air_quality_data.py
```

This step will:

* read all Bronze `csv.gz` files
* clean and filter the dataset
* output Parquet files to the Silver layer

---

# Security

The AWS OpenAQ archive is **public**, so no credentials are required.

Future warehouse access credentials should **never be committed to GitHub**.

---

# Future Improvements

Possible enhancements include:

* ingestion for multiple cities
* automated data quality checks
* CI/CD pipeline
* anomaly detection for pollution spikes
* geospatial pollution analysis
* real-time streaming ingestion

---

# What This Project Demonstrates

This project demonstrates practical data engineering skills including:

* public dataset ingestion
* data lake architecture
* Bronze / Silver / Gold modeling
* data cleaning and transformation
* analytics modeling with dbt
* pipeline orchestration
* dashboard analytics

---
