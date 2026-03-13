# Architecture Decisions

## ADR-001: Fixed five-city scope

Decision:

- keep the project at exactly five cities: London, New York, Delhi, Beijing, and São Paulo

Why:

- enough geographic spread for comparisons
- enough contrast to make the dashboard interesting
- small enough to backfill and explain clearly

## ADR-002: Spark replaces Pandas in the Silver layer

Decision:

- move Bronze to Silver processing from Pandas to Spark

Why:

- the Silver layer now reads many raw archive files, enforces a schema, parses timestamps, standardizes pollutants, enriches metadata, deduplicates rows, and writes partitioned parquet
- this is substantial enough to justify Spark instead of a notebook-style Pandas script

## ADR-003: BigQuery partitioning and clustering

Decision:

- partition the fact table by `measurement_date`
- cluster by `city` and `pollutant`

Why:

- dashboard users filter by date first
- the whole project is built around city comparisons
- pollutant slicing is common in both marts and dashboard tiles

## ADR-004: dbt for marts, not for raw cleanup

Decision:

- use Spark for operational cleanup and dbt for analytical marts

Why:

- Spark is better suited to the file-based Bronze to Silver step
- dbt is better suited to readable warehouse SQL models, tests, and reviewer-facing mart logic
