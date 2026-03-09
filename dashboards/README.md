# Dashboard Guide (Looker Studio)

This file explains how to connect Looker Studio to the project marts.

---

## BigQuery Connection

1. Open Looker Studio and create a new report.
2. Add data source: **BigQuery**.
3. Select project: `aq-pipeline-260309-5800`.
4. Select dataset: `air_quality_dbt_marts`.
5. Add the following tables as data sources:
   - `mart_pollution_by_city`
   - `mart_pollution_by_country`
   - `mart_pollution_trends`
   - `mart_dashboard_daily_city_trends`

---

## Recommended Charts

### 1) Global Trend

Data source: `mart_pollution_trends`

- Dimension: `measurement_date`
- Breakdown dimension: `pollutant`
- Metric: `avg_pollution_value`

Chart type: time series.

### 2) Most Polluted Cities

Data source: `mart_pollution_by_city`

- Dimension: `location_name`
- Breakdown dimension: `pollutant`
- Metric: `avg_pollution_value`
- Optional metric: `peak_pollution_value`

Chart type: bar chart (Top N).

### 3) Polluted Countries (Current Scope)

Data source: `mart_pollution_by_country`

Current ingestion scope is one location, so this table currently behaves as a
portfolio-level pollutant summary. Replace with a true country mart after
multi-country ingestion is added.

- Dimension: `pollutant`
- Metric: `avg_pollution_value`
- Optional metric: `peak_pollution_value`

Chart type: bar chart.

### 4) Pollutant Comparison by City and Date

Data source: `mart_dashboard_daily_city_trends`

- Dimension: `measurement_date`
- Breakdown dimensions: `location_name`, `pollutant`
- Metric: `avg_pollution_value`

Chart type: line chart with filters.

---

## Filters to Add in Dashboard

- Date range filter on `measurement_date`
- Pollutant filter on `pollutant`
- City filter on `location_name`

---

## Refresh Guidance

After pipeline run:

1. Airflow tasks finish (`load_warehouse`, `dbt_run`, `dbt_test`).
2. In Looker Studio, refresh the data source if needed.
3. Validate row counts in each chart.
