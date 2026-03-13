# Review Guide

## What This Project Does

Global City Air Quality Observatory is a batch data engineering project that compares air pollution trends and pollutant patterns across London, New York, Delhi, Beijing, and São Paulo using OpenAQ, GCS, Spark, BigQuery, dbt, Airflow, and Looker Studio.

## Why Five Cities

The project is limited to five cities so the capstone stays focused, analytically interesting, and reviewable in one sitting. The fixed scope gives geographic spread without turning the project into an over-broad global crawl.

## Why Batch, Not Streaming

The source arrives as archive files and the project is designed around scheduled runs. A batch architecture matches the source format and keeps the operational story simple and defensible for the capstone rubric.

## Why Spark Instead Of Pandas

Spark is the main Bronze to Silver engine because the transformation layer now needs schema enforcement, timestamp normalization, pollutant standardization, metadata joins, deduplication, and partitioned parquet output across many raw files.

## What To Check

- Terraform: provisions GCS and BigQuery resources
- Airflow: orchestrates the full batch pipeline in one DAG flow
- Spark: performs the official Bronze to Silver transformation
- BigQuery: stores the warehouse fact and dimensions
- dbt: builds analytical marts for the dashboard
- Looker Studio: presents the five-city comparison dashboard
