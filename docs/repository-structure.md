# Repository Structure

This document explains how the repository is organized.

The goal is to keep the project easy to understand, maintain, and reproduce.

---

## Root Structure

```text
air-quality-data-pipeline/
├── README.md
├── airflow/
├── dashboards/
├── data/
├── dbt/
├── docs/
├── ingestion/
├── processing/
├── terraform/
└── tests/
```

## Key Pipeline Files

```text
ingestion/
  download_air_quality_data.py

processing/
  clean_air_quality_data.py
  check_silver_data_quality.py   # Data quality checks (quality gate)
```
