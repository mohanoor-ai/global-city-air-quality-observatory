# Pipeline Orchestration

This document describes how the data pipeline will be orchestrated.

The pipeline will be orchestrated using **Apache Airflow**.

Airflow will schedule and execute each step of the batch workflow.

---

# Pipeline Overview

The pipeline will run as a scheduled batch job.

The DAG will orchestrate the following stages:

1. extract data from the OpenAQ source
2. store raw files locally
3. upload raw files to Google Cloud Storage
4. clean and transform the raw data
5. store curated data in the data lake
6. load curated data into BigQuery
7. run dbt transformations
8. verify pipeline success

---

# Pipeline DAG

The Airflow DAG will represent the entire workflow.

Example DAG name:

air_quality_batch_pipeline

The DAG will define task dependencies and execution order.

---

# Pipeline Tasks

The pipeline will consist of several tasks.

## Task 1 — Data Extraction

Purpose:

Download air quality measurements from OpenAQ.

Output:

Raw dataset saved locally.

Example script:

ingestion/download_air_quality_data.py

---

## Task 2 — Upload Raw Data

Purpose:

Upload raw files to the raw data lake layer in Google Cloud Storage.

Destination:

gs://air-quality-data-lake/raw/openaq/

---

## Task 3 — Data Cleaning

Purpose:

Transform raw data into a structured format.

Operations may include:

- schema validation
- column renaming
- data type normalization
- removal of invalid records

Output:

Cleaned Parquet files.

Example script:

processing/clean_air_quality_data.py

---

## Task 4 — Upload Curated Data

Purpose:

Upload cleaned data to the curated layer in the data lake.

Destination:

gs://air-quality-data-lake/curated/air_quality/

---

## Task 5 — Load Data into BigQuery

Purpose:

Load curated data into warehouse tables.

Destination dataset example:

air_quality_warehouse

---

## Task 6 — Run dbt Models

Purpose:

Transform warehouse tables into analytics-ready tables.

Example commands:

dbt run
dbt test

---

## Task 7 — Pipeline Validation

Purpose:

Verify that the pipeline completed successfully.

Checks may include:

- verifying row counts
- confirming table updates
- validating dbt tests

---

# Task Dependency Order

The DAG tasks will run in this order:

extract_data
↓
upload_raw_data
↓
clean_data
↓
upload_curated_data
↓
load_bigquery
↓
run_dbt_models
↓
validate_pipeline

---

# Pipeline Schedule

The pipeline will run on a scheduled basis.

Example schedule:

Daily

This allows the dataset to stay up to date with new air quality measurements.

---

# Error Handling

Airflow will handle task failures.

If a task fails:

- the pipeline will stop
- logs will be available in Airflow
- the failed task can be retried

---

# Monitoring

Airflow provides monitoring through:

- task status
- execution logs
- DAG execution history

This allows easy debugging of pipeline failures.

---

# Benefits of Airflow Orchestration

Using Airflow provides:

- automated scheduling
- clear task dependencies
- centralized pipeline monitoring
- retry logic for failed tasks
- reproducible workflows

---

# Future Improvements

Possible future improvements include:

- adding data quality checks
- adding alerts for pipeline failures
- increasing pipeline frequency
- supporting streaming ingestion