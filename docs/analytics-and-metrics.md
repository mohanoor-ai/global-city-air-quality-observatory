# Analytics Goals And Metrics

## Main question

Which countries and cities have the worst PM2.5 exposure over time, and where are trends improving or worsening?

## Dashboard story

1. Global trend over time
2. Worst countries by PM2.5
3. Worst cities by PM2.5
4. Pollutant comparison across locations

## Core metrics

- average PM2.5 by country
- average PM2.5 by city
- monthly PM2.5 trend over time
- highest recorded pollutant value by location
- pollutant distribution by type

## Mart mapping

- `mart_pm25_by_country`
  - grain: `month_start, country`
  - key metrics: `avg_pm25`, `max_pm25`, `measurement_count`

- `mart_pm25_by_city`
  - grain: `month_start, country, city`
  - key metrics: `avg_pm25`, `max_pm25`, `measurement_count`

- `mart_pollution_trends`
  - grain: `month_start, pollutant`
  - key metrics: `avg_value`, `max_value`, `measurement_count`

- `mart_pollutant_distribution`
  - grain: `country, city, pollutant`
  - key metrics: `measurement_count`, `avg_value`, `median_value`, `p95_value`, `max_value`

- `mart_extreme_pollution_events`
  - grain: event row
  - key fields: timestamp, location, pollutant, value, `pollutant_rank`

## Current limitation

Country/city coverage depends on rows in `ingestion/location_targets.csv`.  
The current setup uses one major city per inhabited continent (6 total) as a global starter scope.  
To improve ranking depth, add more cities per continent.
