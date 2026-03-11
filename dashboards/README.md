# Dashboard Guide (Looker Studio)

Connect Looker Studio to dataset `air_quality_dbt_marts` in project `aq-pipeline-260309-5800`.

Use these marts:

- `mart_pm25_by_country`
- `mart_pm25_by_city`
- `mart_pollution_trends`
- `mart_pollutant_distribution`
- `mart_extreme_pollution_events`

## Suggested Dashboard Pages

1. Global trend
- Data source: `mart_pollution_trends`
- Dimension: `month_start`
- Breakdown: `pollutant`
- Metric: `avg_value`

2. Worst countries
- Data source: `mart_pm25_by_country`
- Dimension: `country`
- Metric: `avg_pm25`

3. Worst cities
- Data source: `mart_pm25_by_city`
- Dimensions: `country`, `city`
- Metric: `avg_pm25`

4. Pollutant comparison
- Data source: `mart_pollutant_distribution`
- Dimensions: `pollutant`, `country` or `city`
- Metrics: `median_value`, `p95_value`, `max_value`

5. Extreme events table
- Data source: `mart_extreme_pollution_events`
- Dimensions: `measurement_datetime`, `country`, `city`, `pollutant`
- Metric: `value`

## Filters

- Date filter on `month_start` or `measurement_datetime`
- Pollutant filter
- Country / city filters

## Screenshot Evidence

Save dashboard screenshots under `images/` using these names:

- `images/dashboard_global_trend.png`
- `images/dashboard_worst_countries.png`
- `images/dashboard_worst_cities.png`
- `images/dashboard_pollutant_comparison.png`
- `images/dashboard_extreme_events.png`

Current status: pending capture.
