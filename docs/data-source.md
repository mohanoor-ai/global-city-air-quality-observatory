# Data Source

This project uses the OpenAQ AWS archive:

- Registry page: https://registry.opendata.aws/openaq/
- Archive docs: https://docs.openaq.org/aws/about
- Bucket: `s3://openaq-data-archive`

## Source File Pattern

The ingestion script reads compressed CSV files under:

```text
records/csv.gz/locationid=<location_id>/year=<yyyy>/month=<mm>/
```

Example:

```text
records/csv.gz/locationid=2178/year=2026/month=03/location-2178-20260309.csv.gz
```

## Why This Source

- Historical backfill is straightforward because files are partitioned by year/month
- Daily incremental ingestion is straightforward by taking the newest file per location
- The same source supports PM2.5-focused analytics and pollutant comparison

## Practical Note

In this repository, location-to-city/country mapping is managed with:

`ingestion/location_targets.csv`

This keeps the ingestion logic simple and transparent for project review.
