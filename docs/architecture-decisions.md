# Architecture Decisions

This note records the main choices used in the current repo.

## 1) Batch pipeline, not streaming

Decision:
- Keep the project batch-oriented for simpler operations.

Why:
- The source already provides daily archive files.
- Backfill and daily incremental runs are enough for the project question.

## 2) OpenAQ AWS archive over API polling

Decision:
- Ingest from `s3://openaq-data-archive` `csv.gz` files.

Why:
- File partitions by location/year/month make backfill straightforward.
- Daily mode can pick the newest file per configured location.

## 3) Simple medallion flow

Decision:
- Bronze: raw `csv.gz` files.
- Silver: cleaned parquet.
- Gold: dbt marts.

Why:
- Easy to explain and debug.
- Uses a clear layered data flow without extra layers.

## 4) PM2.5-first marts with pollutant comparison

Decision:
- Keep PM2.5 as the main analytical focus.
- Still include other pollutants for trends/distribution.

Why:
- Matches the project question.
- Supports both focused and comparative dashboard views.

## 5) Modest orchestration

Decision:
- Two Airflow entrypoints:
  - backfill DAG (manual trigger)
  - daily DAG (`@daily`)

Why:
- Clear operational split.
- No advanced scheduling complexity.
