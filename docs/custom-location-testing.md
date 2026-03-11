# Custom Location Testing

Use this when you want to run the pipeline for your own city list instead of the default `ingestion/location_targets.csv`.

## Where to find city and location IDs

Use OpenAQ AWS archive docs (no API key required):

- AWS quick start: https://docs.openaq.org/aws/quick-start
- Year guide example: https://docs.openaq.org/aws/year-guide

Archive key pattern used by this project:

```text
s3://openaq-data-archive/records/csv.gz/locationid=<id>/year=<yyyy>/month=<mm>/
```

### Fast way to find location IDs by city keyword (AWS only)

Run this command from project root:

```bash
uv run python ingestion/find_location_ids_from_aws.py --keyword delhi --max-matches 10
```

It prints:

```text
location_id,location_name
8118,Delhi US Diplomatic P...
...
```

Then copy one `location_id` you trust and map it to your own `city,country` row in the targets CSV.

## 1) Create a custom targets file

Create a CSV anywhere on your machine with this schema:

```csv
location_id,city,country
8118,Delhi,IN
159,London,GB
```

Required columns:

- `location_id`
- `city`
- `country`

## 2) Run ingestion with the custom file

Daily incremental test:

```bash
uv run python ingestion/download_air_quality_data.py --mode daily --targets-file /path/to/my_targets.csv
```

Historical backfill test:

```bash
uv run python ingestion/download_air_quality_data.py --mode backfill --targets-file /path/to/my_targets.csv
```

## 3) Continue the local pipeline

```bash
uv run python processing/clean_air_quality_data.py
uv run python processing/check_silver_data_quality.py
```

Optional cloud steps:

```bash
uv run python warehouse/load_to_bigquery.py
```

Then run dbt from `dbt/air_quality_project` if your cloud credentials are configured.

## Notes

- This does not require code changes.
- The script also writes `data/bronze/location_metadata.csv` from your custom file, so city and country values flow into Silver and marts.
- If a `location_id` has no files in the archive, ingestion will log a warning and continue.
