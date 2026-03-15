# Architecture Decisions

## ADR-001: Fixed Five-City Scope

Decision:

- keep the project limited to London, New York, Delhi, Beijing, and Berlin

Why:

- this avoids an over-broad global analysis story
- the five-city comparison is easier to validate and explain
- the dashboard remains readable during review

## ADR-002: Batch Architecture

Decision:

- use a scheduled batch pipeline rather than streaming

Why:

- the source is delivered as archive files
- the project is orchestrated on a schedule
- batch is a better fit for this capstone than a streaming system

## ADR-003: Spark Replaces Pandas For Bronze To Silver

Decision:

- make Spark the main Bronze to Silver transformation engine

Why:

- the Silver layer requires schema enforcement, timestamp parsing, pollutant standardization, metadata enrichment, deduplication, and parquet output
- Spark is a better fit for repeatable batch transformation at this stage than a notebook-style Pandas cleanup flow

## ADR-004: BigQuery Table Optimization

Decision:

- partition BigQuery fact tables by `measurement_date`
- cluster by `city` and `pollutant`

Why:

- reviewer-facing queries filter by date
- the project centers on city comparison
- pollutant slicing is common in marts and dashboard pages

## ADR-005: dbt For Analytical Marts

Decision:

- use dbt for analytical marts rather than raw-data cleaning

Why:

- Spark is the right place for operational Bronze to Silver standardization
- dbt is the right place for readable, testable analytical marts
