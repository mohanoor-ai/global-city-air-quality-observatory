# Global City Air Quality Observatory

## Problem statement

This project asks a focused analytics question:

How do pollution trends and pollutant patterns differ across five major global cities over time?

It is a batch end-to-end data engineering capstone built for the Data Engineering Zoomcamp project rubric. The repo is intentionally centered on one reviewer-friendly story instead of broad "global air quality" coverage. A reviewer should be able to identify where the data comes from, how it lands in a data lake, how it moves into the warehouse, how it is transformed, how it is visualized, and how someone else can run it.

## Why these five cities

The fixed city scope is:

- London, United Kingdom
- New York, United States
- Delhi, India
- Beijing, China
- São Paulo, Brazil

I narrowed the project to exactly five cities for five reasons:

- global geographic spread across Europe, North America, Asia, and South America
- clear analytical contrast between lower and higher pollution baselines
- stronger monitoring availability than a fully open-ended city list
- a dashboard that stays readable during a capstone demo
- a manageable scope for backfill, validation, and reproducibility

The city list is locked in [ingestion/location_targets.csv](/home/moha_/projects/global-city-air-quality-observatory/ingestion/location_targets.csv) and validated by [ingestion/city_scope.py](/home/moha_/projects/global-city-air-quality-observatory/ingestion/city_scope.py).

## Architecture diagram

Architecture image: [images/architecture_diagram.svg](/home/moha_/projects/global-city-air-quality-observatory/images/architecture_diagram.svg)

```text
OpenAQ AWS archive
    -> Python ingestion
    -> GCS Bronze raw files
    -> Spark Bronze to Silver standardization
    -> Silver parquet quality checks
    -> BigQuery fact and dimension tables
    -> dbt staging and marts
    -> Looker Studio dashboard
```

## What this project demonstrates

- batch ingestion from a public source archive
- medallion-style lake design with Bronze and Silver layers
- meaningful Spark use for schema enforcement, timestamp normalization, city filtering, metadata enrichment, and deduplication
- warehouse loading into partitioned and clustered BigQuery tables
- dbt models that turn warehouse measurements into dashboard-ready marts
- Airflow orchestration for both backfill and daily refresh flows
- Terraform-managed cloud resources on GCP

## Data source

The source is the OpenAQ historical archive hosted in AWS Open Data. The ingestion script reads `csv.gz` files from `s3://openaq-data-archive/records/csv.gz/locationid=.../year=.../month=.../`.

Key source details:

- format: raw `csv.gz` files
- ingestion mode: batch only
- backfill strategy: last two full years plus current year to date
- daily strategy: latest available file per configured city location

Relevant files:

- [ingestion/download_air_quality_data.py](/home/moha_/projects/global-city-air-quality-observatory/ingestion/download_air_quality_data.py)
- [docs/data-source.md](/home/moha_/projects/global-city-air-quality-observatory/docs/data-source.md)

## Data lake ingestion

Python handles source download and lands minimally changed files in Bronze. Bronze keeps the raw archive layout for traceability. Metadata for the five-city scope is also written into Bronze so the Spark job can enrich measurements with city and country fields.

Bronze:

- grain: raw source file
- storage: GCS bucket `bronze/` prefix and local `data/bronze/`
- change level: minimal

Silver:

- grain: one row per city, station, timestamp, pollutant measurement
- storage: partitioned parquet in `silver/air_quality_measurements/`
- produced by: [spark/bronze_to_silver.py](/home/moha_/projects/global-city-air-quality-observatory/spark/bronze_to_silver.py)

Spark handles:

- reading Bronze raw files
- schema enforcement
- timestamp parsing and normalization
- pollutant standardization
- filtering to the fixed five-city scope
- metadata enrichment
- deduplication
- writing partitioned Silver parquet

## Warehouse loading

The warehouse is BigQuery. The load step uploads the Silver parquet dataset to GCS, loads a staging table, then rebuilds the curated warehouse tables.

Core warehouse tables:

- `fct_air_quality_measurements`
- `dim_city`
- `dim_pollutant`

Fact table design:

- grain: one row per city, station, timestamp, pollutant measurement
- partitioning: `measurement_date`
- clustering: `city`, `pollutant`

That layout matches the dashboard access pattern:

- dashboard users filter by time
- city comparisons are central to the project question
- pollutant comparisons are also central

Relevant file:

- [warehouse/load_to_bigquery.py](/home/moha_/projects/global-city-air-quality-observatory/warehouse/load_to_bigquery.py)

## Transformations

There are two transformation layers.

Spark Silver layer:

- standardizes raw source fields into an analysis-ready measurement table
- keeps row-level detail
- performs operational cleanup before warehouse load

dbt layer:

- stages warehouse data in [dbt/air_quality_project/models/staging/stg_air_quality.sql](/home/moha_/projects/global-city-air-quality-observatory/dbt/air_quality_project/models/staging/stg_air_quality.sql)
- builds marts for dashboard queries

Main dbt marts:

- `mart_city_pollution_trends`
  grain: one row per city, pollutant, measurement date
  purpose: temporal trend analysis across cities
- `mart_city_pollutant_distribution`
  grain: one row per city and pollutant
  purpose: categorical comparison of average and percentile pollutant levels
- `mart_city_extreme_events`
  grain: one row per ranked city-pollutant extreme event
  purpose: inspect spikes and unusual readings
- `mart_city_comparison_summary`
  grain: one row per city
  purpose: scorecard view for cross-city comparison
- `mart_pm25_city_daily`
  grain: one row per city and date
  purpose: feed the main PM2.5 trend chart

## Dashboard

The dashboard is a Looker Studio city comparison dashboard built around the fixed five-city question.

Required tiles:

- pollution trend over time
  chart: line chart
  mart: `mart_pm25_city_daily`
  question answered: how has daily PM2.5 changed by city over time?
- pollutant distribution by city
  chart: bar chart or stacked bar chart
  mart: `mart_city_pollutant_distribution`
  question answered: which pollutants dominate each city's measurement profile?

Optional supporting tiles:

- extreme pollution events
  mart: `mart_city_extreme_events`
- city comparison scorecard
  mart: `mart_city_comparison_summary`

Dashboard docs and screenshots:

- [dashboards/README.md](/home/moha_/projects/global-city-air-quality-observatory/dashboards/README.md)
- [images/dashboard_pm25_trend.png](/home/moha_/projects/global-city-air-quality-observatory/images/dashboard_pm25_trend.png)
- [images/dashboard_pollutant_distribution.png](/home/moha_/projects/global-city-air-quality-observatory/images/dashboard_pollutant_distribution.png)

## How to run

The full setup and execution steps are in [runbook.md](/home/moha_/projects/global-city-air-quality-observatory/runbook.md).

Short version:

```bash
uv sync
uv run python ingestion/download_air_quality_data.py --mode backfill
uv run python spark/bronze_to_silver.py --write-mode overwrite
uv run python spark/check_silver_data_quality.py
uv run python warehouse/load_to_bigquery.py
bash scripts/dbt_run.sh
bash scripts/dbt_test.sh
```

Airflow DAGs:

- `global_city_air_quality_backfill`
- `global_city_air_quality_daily`

## Tech stack

- Cloud: GCP
- Infrastructure as code: Terraform
- Orchestration: Airflow
- Ingestion: Python
- Batch processing: Spark
- Data lake: GCS Bronze and Silver
- Warehouse: BigQuery
- Transformations: Spark and dbt
- Dashboard: Looker Studio
- Environment tooling: `uv`

## How this project meets the Zoomcamp rubric

- Problem description -> this README problem statement and the fixed five-city rationale
- Cloud -> GCP resources provisioned with Terraform for GCS and BigQuery
- Data ingestion / orchestration -> Python ingestion plus Airflow DAGs landing Bronze files and orchestrating the full batch pipeline
- Data warehouse -> BigQuery fact and dimension tables with partitioning and clustering
- Transformations -> Spark Silver standardization plus dbt staging and marts
- Dashboard -> Looker Studio dashboard with a temporal trend tile and a categorical distribution tile
- Reproducibility -> this README, [runbook.md](/home/moha_/projects/global-city-air-quality-observatory/runbook.md), [.env.example](/home/moha_/projects/global-city-air-quality-observatory/.env.example), Terraform, and runnable commands

## Limitations

- coverage depends on the chosen OpenAQ locations for each city
- unit harmonization is limited to the source values already present in the archive
- the daily pipeline is batch-incremental, not real-time streaming
- city-level averages can hide station-level differences inside each metro area

## Lessons learned

Short version:

- narrowing the scope made the project easier to explain and validate
- Spark became worthwhile once the Silver layer needed schema enforcement and repeatable batch transformations across many raw files
- BigQuery partitioning and clustering mattered because the dashboard always filters by date, city, and pollutant

Full notes:

- [docs/lessons-learned.md](/home/moha_/projects/global-city-air-quality-observatory/docs/lessons-learned.md)
- [docs/architecture-decisions.md](/home/moha_/projects/global-city-air-quality-observatory/docs/architecture-decisions.md)
- [docs/reviewer-guide.md](/home/moha_/projects/global-city-air-quality-observatory/docs/reviewer-guide.md)
