# Project Plan

## Project Name

Global Air Quality Data Pipeline

---

## Project Goal

Build an end-to-end batch data pipeline for global air quality data.

The pipeline will:

1. collect air quality data from OpenAQ
2. convert the data into a structured format
3. store the data in a cloud data lake
4. load the data into a cloud data warehouse
5. transform the data using dbt
6. orchestrate the workflow using Airflow
7. visualize the results in a dashboard

---

## Main Questions the Project Should Answer

The project should help answer questions such as:

- Which countries have the highest pollution levels?
- How does air quality change over time?
- Which cities have the worst air pollution?
- Which pollutants are most common?
- Are pollution levels improving or worsening?

---

## Data Source

Source: OpenAQ

Data type:

- air quality measurements
- pollutants such as PM2.5, PM10, NO2, SO2, CO, and O3
- location and timestamp information

---

## Final Architecture

The project will follow this architecture:

OpenAQ  
→ Python ingestion  
→ Parquet files  
→ Google Cloud Storage  
→ BigQuery  
→ dbt  
→ Looker Studio  
→ Airflow orchestration

---

## Tools Used

### Orchestration
- Apache Airflow

### Ingestion
- Python

### Data Lake
- Google Cloud Storage

### Data Warehouse
- BigQuery

### Transformations
- dbt

### Infrastructure
- Terraform

### Dashboard
- Looker Studio

### Containerization
- Docker

---

## Project Structure

```text
air-quality-data-pipeline/

README.md

airflow/
ingestion/
processing/
dbt/
terraform/
dashboards/
docs/
tests/
data/