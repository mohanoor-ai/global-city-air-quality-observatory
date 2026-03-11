# Data Lake Design

The project keeps a simple two-layer local lake, with optional cloud copy.

## Local layers

- `data/bronze/`: raw OpenAQ archive files (`csv.gz`)
- `data/silver/`: cleaned parquet from processing script

Bronze keeps source files unchanged. Silver applies light cleaning and keeps analysis fields (`country`, `city`, `pollutant`, `measurement_datetime`, `value`).

## Bronze layout

Bronze mirrors source keys:

```text
data/bronze/records/csv.gz/locationid=<id>/year=<yyyy>/month=<mm>/...
```

The ingestion step also writes:

```text
data/bronze/location_metadata.csv
```

This metadata is generated from `ingestion/location_targets.csv` and used in Silver enrichment.

## Cloud copy (when used)

When cloud upload is enabled, the same `bronze/` and `silver/` prefixes are used in GCS.

## Why this design

- easy to explain during review
- easy to inspect locally
- enough structure for backfill and daily runs without extra complexity
