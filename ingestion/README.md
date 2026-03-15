# Ingestion Layer

This folder contains Bronze ingestion for OpenAQ archive files.

## Modes

- `backfill`: downloads last 2 full years plus current year-to-date
- `daily`: downloads only the newest available file per configured location

## Location Targets

`location_targets.csv` controls city/country scope.

Required columns:

- `location_id`
- `city`
- `country`

The script writes `data/bronze/location_metadata.csv` from this file so downstream processing can preserve city and country fields.

Current starter scope is a fixed cross-region comparison chosen to keep the project lightweight while still comparable across different urban contexts.

## Commands

Find location IDs by city keyword (AWS archive, no API key):

```bash
uv run python ingestion/find_location_ids_from_aws.py --keyword delhi --max-matches 10
```

Backfill:

```bash
uv run python ingestion/download_air_quality_data.py --mode backfill
```

Daily:

```bash
uv run python ingestion/download_air_quality_data.py --mode daily
```

Optional:

```bash
uv run python ingestion/download_air_quality_data.py --mode backfill --overwrite
```

## Output

Raw files are stored in Bronze with the OpenAQ key structure:

```text
data/bronze/records/csv.gz/locationid=<id>/year=<yyyy>/month=<mm>/...
```
