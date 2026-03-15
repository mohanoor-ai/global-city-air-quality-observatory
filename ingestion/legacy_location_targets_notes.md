# Location Targets Notes

This file documents how `ingestion/location_targets.csv` was prepared.

## How location IDs were found

Method used:

- OpenAQ AWS archive scan (no API key)
- Helper command:

```bash
uv run python ingestion/find_location_ids_from_aws.py --keyword <city_keyword> --max-matches 10
```

The command prints candidate rows in this format:

```text
location_id,location_name
```

Then one valid `location_id` was selected per city and added to `location_targets.csv` with explicit `city,country` metadata.

## Current selected locations

- London, GB (`location_id=159`)
- New York, US (`location_id=2451`)
- Delhi, IN (`location_id=8118`)
- Beijing, CN (`location_id=1451`)
- Berlin, DE (`location_id=3019`)

## Why this selection

- fixed five-city comparison with strong policy and pollution contrast
- keeps ingestion volume manageable
- supports reviewer-friendly comparison across different urban contexts
