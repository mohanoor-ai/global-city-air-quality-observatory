# Reviewer guide

## What this project does

This project compares air pollution trends and pollutant patterns across five major global cities using a batch data engineering pipeline.

## Why these five cities

The project uses London, New York, Delhi, Beijing, and Berlin to keep the scope fixed and make cross-city comparison meaningful.

## Why batch

The source data is processed on scheduled intervals, so a batch architecture is appropriate.

## Why Spark

Spark is used in the Bronze to Silver layer to demonstrate distributed data transformation instead of relying on Pandas.

## What the reviewer should check

- Terraform provisions cloud resources
- Airflow orchestrates the pipeline
- Spark builds Silver data
- BigQuery stores curated warehouse data
- dbt builds marts
- Looker Studio visualizes outputs
