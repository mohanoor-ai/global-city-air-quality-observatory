# Analytics Goals and Metrics

This document defines the analytical goals of the project.

It explains what insights the pipeline should produce and what metrics will appear in the dashboard.

The analytics layer will be built using BigQuery and dbt.

---

# Purpose of the Analytics Layer

The goal of the analytics layer is to transform raw air quality measurements into structured tables that allow easy analysis and visualization.

These tables will support the final dashboard and help answer key questions about air pollution.

---

# Key Questions

The project should allow us to answer questions such as:

- Which countries have the highest pollution levels?
- Which cities have the worst air quality?
- How does pollution change over time?
- Which pollutants are most common?
- Are pollution levels improving or worsening?

---

# Key Metrics

The dashboard should focus on several core metrics.

## Average Pollution Level

Average pollution level for each pollutant.

Example:

Average PM2.5 level by country.

---

## Maximum Pollution Level

Highest recorded pollution value in a time period.

Example:

Highest PM2.5 level recorded in a city.

---

## Pollution Trends Over Time

Average pollution level by:

- day
- month
- year

This helps identify long-term trends.

---

## Pollution by Country

Average pollution levels grouped by country.

This helps identify geographic differences.

---

## Pollution by City

Average pollution levels grouped by city.

This allows comparison between urban areas.

---

## Pollutant Distribution

Distribution of measurements across pollutant types.

Example:

- PM2.5
- PM10
- NO2
- SO2
- CO
- O3

---

# Data Dimensions

The analytics tables will use several important dimensions.

## Time

- timestamp
- date
- month
- year

## Location

- country
- city
- coordinates

## Pollutant

- pollutant type
- measurement unit

---

# Data Fact

The main fact stored in the warehouse will be pollution measurements.

Example fields:

- timestamp
- pollutant
- measurement value
- unit
- location

---

# Planned Warehouse Tables

The warehouse will contain several tables.

## Fact Table

fact_air_quality_measurements

Contains individual pollution measurements.

Example columns:

- timestamp
- pollutant
- value
- unit
- city
- country
- latitude
- longitude


## Dimension Table — Locations

dim_locations

Contains information about measurement locations.

Example fields:

- location id
- city
- country
- latitude
- longitude

## Dimension Table — Pollutants

dim_pollutants

Contains information about pollutant types.

Example fields:

- pollutant name
- pollutant description
- unit

---

# dbt Model Layers

## Staging Layer

The staging layer will clean and standardize raw warehouse data.

Example model:

stg_air_quality_measurements

This layer will:

- rename columns
- standardize data types
- clean raw values
- make source data easier to use downstream

---

## Intermediate Layer

The intermediate layer will join and enrich the data.

Example model:

int_measurements_enriched

This layer will:

- combine measurement data with location information
- prepare data for marts
- simplify repeated transformation logic

---

## Mart Layer

The mart layer will create analytics-ready tables for reporting and dashboards.

Example models:

- mart_pollution_by_country
- mart_pollution_by_city
- mart_pollution_trends

These tables will be used directly in the dashboard.

---

# Dashboard Visualizations

The dashboard will likely include:

## Global Pollution Overview

A map or summary showing pollution levels by country.

---

## Pollution Trends

A line chart showing how pollution changes over time.

---

## Top Polluted Cities

A bar chart showing cities with the highest pollution levels.

---

## Pollutant Comparison

A comparison of major pollutants such as PM2.5, PM10, and NO2.

---

# Success Criteria

The analytics layer is successful when:

- raw measurements are transformed into structured warehouse tables
- dbt models run successfully
- warehouse tables support dashboard queries
- metrics are easy to understand
- insights are clearly visible in the final dashboard

---

# Guiding Principle

The analytics layer should remain:

- simple
- well structured
- easy to query
- easy to visualize
- aligned with the goals of the project