# Project guide

## What this project does

This project compares air pollution trends and pollutant patterns across five major global cities using a batch data engineering pipeline.

## Problem Statement

Air quality monitoring matters because pollution affects public health, daily
life, and long-term policy decisions. A city-level comparison can show how
pollutant patterns change over time, where conditions are improving or
worsening, and which pollutants dominate in different urban environments.

This project answers that need with a fixed five-city comparison built for
reviewability and reproducibility rather than a broad global ranking exercise.

## Why these five cities

The project uses London, New York, Delhi, Beijing, and Berlin to keep the scope fixed and make cross-city comparison meaningful.

## Why batch

The source data is processed on scheduled intervals, so a batch architecture is appropriate.

## Why Spark

Spark is used in the Bronze to Silver layer to demonstrate distributed data transformation instead of relying on Pandas.

## What to check

- Terraform provisions cloud resources
- Airflow orchestrates the pipeline
- Spark builds Silver data
- BigQuery stores curated warehouse data
- dbt builds marts
- Looker Studio visualizes outputs
