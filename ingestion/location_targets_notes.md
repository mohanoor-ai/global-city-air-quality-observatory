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

- Cairo, EG (`location_id=1621200`)
- Delhi, IN (`location_id=8118`)
- London, GB (`location_id=159`)
- Mexico City, MX (`location_id=3350392`)
- Buenos Aires, AR (`location_id=2847299`)
- Sydney, AU (`location_id=2392564`)

## Why this selection

- one major city per inhabited continent
- keeps ingestion volume manageable
- supports globally relatable comparisons
