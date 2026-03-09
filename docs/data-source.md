# Data Source

This document describes the dataset used in the project.

---

## Source

The data comes from **OpenAQ**.

OpenAQ is a platform that provides open air quality measurements from monitoring stations around the world.

Website:

https://openaq.org

---

## Why This Dataset

This dataset is useful because it contains real-world environmental measurements that can be used to analyze pollution trends.

It allows us to answer questions such as:

- which countries have the highest pollution levels
- how pollution changes over time
- which pollutants are most common
- which areas are more affected than others

This makes it a good dataset for an end-to-end data engineering project.

---

## Data Access Method

The project uses OpenAQ as the source of air quality measurements.

The data is accessed through:

- API-based extraction
- structured ingestion pipeline

The ingestion step will pull data from OpenAQ and convert it into a format suitable for analytics.

---

## Main Pollutants

The dataset includes measurements for pollutants such as:

- PM2.5
- PM10
- NO2
- SO2
- CO
- O3

These pollutants are commonly used in air quality analysis.

---

## Important Fields

The exact schema may vary depending on the API response, but the project is mainly interested in fields related to:

- pollutant name
- measurement value
- measurement unit
- timestamp
- location or city
- country
- coordinates

These are the fields needed to build analytics tables and dashboards.

---

## Fields We Intend to Keep

The project will focus on fields needed for analysis and reporting.

Examples of useful fields include:

- measurement timestamp
- pollutant
- value
- unit
- city
- country
- latitude
- longitude

---

## Fields We May Ignore

The source may include metadata fields that are not important for the dashboard or warehouse model.

Examples may include:

- technical API metadata
- fields not needed for analytics
- duplicate nested information

These can be dropped during the cleaning and transformation stages.

---

## Expected Data Volume

The OpenAQ platform contains a large volume of data collected from many stations across many countries.

This makes it suitable for demonstrating:

- ingestion
- cloud storage
- warehousing
- transformations
- orchestration
- dashboarding

---

## Role in the Pipeline

The OpenAQ data is the starting point of the project.

The planned flow is:

OpenAQ  
→ Python ingestion  
→ Parquet files  
→ Google Cloud Storage  
→ BigQuery  
→ dbt  
→ Dashboard

---

## Notes

As the project develops, this document should be updated with:

- confirmed source endpoints
- exact fields extracted
- example records
- final schema decisions