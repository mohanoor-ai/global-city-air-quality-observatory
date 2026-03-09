# Architecture Decisions

This document records the key design decisions made for the project.

The goal is to keep the project aligned with the methodology and coding style used in the Data Engineering Zoomcamp.

---

## 1. Project Style and Methodology

This project follows the conventions used in the Data Engineering Zoomcamp.

That means:

- the project should be simple and easy to understand
- the project should use clear folder structure
- the project should follow batch data engineering patterns
- the implementation should be reproducible
- the code and documentation should be beginner-friendly
- the architecture should be easy to explain during project review

We do not want an over-engineered project.

We want a project that is complete, clean, and understandable.

---

## 2. Orchestration Choice

The original design used Kestra for orchestration.

For this project, we decided to use **Apache Airflow** instead.

### Reason

Airflow is more aligned with the Zoomcamp style and is easier to justify as part of a traditional batch data pipeline project.

### Decision

We will keep the rest of the architecture the same, but replace Kestra with Airflow.

---

## 3. Ingestion Strategy

The OpenAQ API returns data in JSON format.

However, Zoomcamp projects do not typically keep JSON as the main storage format.

### Reason

In the Zoomcamp workflow, the usual pattern is:

1. ingest raw data
2. convert to a structured format
3. store as Parquet
4. load into the warehouse
5. transform with dbt

### Decision

We will **not store JSON as the main raw format in the pipeline**.

Instead, we will:

- fetch the data from the API
- convert it into a structured tabular format
- save it as **Parquet**

This is more consistent with the course methodology.

---

## 4. Storage Format

We will use **Parquet** as the main storage format.

### Reason

Parquet is better suited for data engineering workflows because:

- it is columnar
- it is smaller than CSV and JSON
- it is faster for analytics
- it works well with BigQuery
- it follows modern data engineering practice

### Decision

The raw and processed layers of the project will use Parquet wherever possible.

---

## 5. Pipeline Type

This project will use a **batch pipeline**.

### Reason

Batch processing is simpler, easier to explain, and more suitable for the project scope.

It also aligns well with Zoomcamp modules related to orchestration, warehousing, and analytics engineering.

### Decision

The pipeline will run on a schedule using Airflow.

Streaming may be considered as a future improvement, but it is not part of the core implementation.

---

## 6. Core Architecture

The project architecture will follow this pattern:

OpenAQ Data Source  
→ Python Ingestion  
→ Parquet Files  
→ Google Cloud Storage  
→ BigQuery  
→ dbt  
→ Looker Studio  
→ Airflow orchestration

This keeps the project modern, cloud-based, and aligned with Zoomcamp expectations.

---

## 7. Project Goal

The purpose of the project is to build an end-to-end data engineering pipeline for global air quality data.

The pipeline should allow us to answer questions such as:

- which countries have the highest pollution levels
- how air quality changes over time
- which cities are most affected
- which pollutants are most significant

---

## 8. Guiding Principle

The project must be:

- complete
- easy to follow
- well documented
- reproducible
- consistent with Zoomcamp conventions
- understandable to reviewers and recruiters