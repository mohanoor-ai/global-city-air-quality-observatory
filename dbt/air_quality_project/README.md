# dbt - air_quality_project

This dbt project builds analytical marts on top of the BigQuery warehouse tables
loaded by `warehouse/load_to_bigquery.py`.

---

## Model structure

```text
models/
  sources.yml
  staging/
    stg_air_quality.sql
    stg_air_quality.yml
  marts/
    reporting/
      mart_city_pollution_trends.sql
      mart_city_pollutant_distribution.sql
      mart_city_extreme_events.sql
      mart_city_comparison_summary.sql
      mart_pm25_city_daily.sql
      marts.yml
tests/
  mart_city_comparison_summary_has_supported_metric.sql
```

---

## What each model does

### `stg_air_quality`

Reads the warehouse fact table and standardizes the measurement-level fields
used by the marts. This is the only staging model in the project.

```sql
select
  city,
  country,
  measurement_datetime,
  measurement_date,
  location_id,
  location_name,
  sensor_id,
  latitude,
  longitude,
  lower(pollutant) as pollutant,
  cast(measurement_value as float64) as measurement_value,
  measurement_unit,
  batch_date,
  source_file
from {{ source('warehouse', 'fct_air_quality_measurements') }}
```

### `mart_city_pollution_trends`

Builds the daily city-and-pollutant trend grain used for the time-series view.

```sql
select
  measurement_date,
  city,
  country,
  pollutant,
  round(avg(measurement_value), 3) as avg_measurement_value,
  max(measurement_value) as max_measurement_value,
  count(*) as measurement_count
from {{ ref('stg_air_quality') }}
group by 1, 2, 3, 4
```

### `mart_city_pollutant_distribution`

Aggregates pollutant profiles by city with average, median, p95, and row counts.

```sql
select
  city,
  country,
  pollutant,
  round(avg(measurement_value), 3) as avg_measurement_value,
  approx_quantiles(measurement_value, 100)[offset(50)] as median_measurement_value,
  approx_quantiles(measurement_value, 100)[offset(95)] as p95_measurement_value,
  count(*) as measurement_count
from {{ ref('stg_air_quality') }}
group by 1, 2, 3
```

### `mart_city_extreme_events`

Ranks the highest readings per city and pollutant and keeps the top 10 events
for anomaly review.

```sql
with ranked_events as (
    select
      measurement_datetime,
      measurement_date,
      city,
      country,
      location_name,
      pollutant,
      measurement_value,
      measurement_unit,
      row_number() over (
        partition by city, pollutant
        order by measurement_value desc, measurement_datetime desc
      ) as city_pollutant_rank
    from {{ ref('stg_air_quality') }}
)
select *
from ranked_events
where city_pollutant_rank <= 10
```

### `mart_city_comparison_summary`

Produces one summary row per city with pollutant averages, latest coverage date,
and measurement counts.

```sql
select
  city,
  country,
  round(avg(case when pollutant = 'pm25' then measurement_value end), 3) as avg_pm25,
  round(avg(case when pollutant = 'pm10' then measurement_value end), 3) as avg_pm10,
  round(avg(case when pollutant = 'no2' then measurement_value end), 3) as avg_no2,
  max(measurement_date) as latest_measurement_date,
  count(*) as measurement_count
from {{ ref('stg_air_quality') }}
group by 1, 2
```

### `mart_pm25_city_daily`

Specialized daily PM2.5 trend table used for the main line-chart view.

```sql
select
  measurement_date,
  city,
  country,
  round(avg(measurement_value), 3) as avg_pm25,
  max(measurement_value) as max_pm25,
  count(*) as measurement_count
from {{ ref('stg_air_quality') }}
where pollutant = 'pm25'
group by 1, 2, 3
```

---

## Tests

The project includes schema tests and one custom data test.

`stg_air_quality.yml` covers:

- `not_null` on `city`, `country`, `measurement_datetime`, `measurement_date`, `location_id`, `location_name`, `pollutant`, and `measurement_value`
- `accepted_values` on `pollutant` for `pm25`, `pm10`, `no2`, `co`, and `o3`

`marts.yml` covers:

- `not_null` checks on the primary reporting columns across all five marts

`tests/mart_city_comparison_summary_has_supported_metric.sql` ensures each city
summary row has at least one populated pollutant average.

Run all models and tests:

```bash
bash scripts/dbt_run.sh
bash scripts/dbt_test.sh
```

---

## Materialization

Materialization is defined in `dbt_project.yml`:

- staging models materialize as `view`
- mart models materialize as `table`

The project writes staging models to the `staging` schema and marts to the
`marts` schema.
