# Zero To Hero Tutorial

This tutorial teaches the project from first principles and walks all the way from idea to runnable pipeline.

By the end, you should understand how Global City Air Quality Observatory works, why each tool is used, how to run each stage, and what evidence to collect for a reviewer.

## 1. What We Are Building

Global City Air Quality Observatory is a batch data engineering project that compares air pollution trends and pollutant patterns across London, New York, Delhi, Beijing, and Berlin using OpenAQ, GCP, Spark, BigQuery, dbt, Airflow, and Looker Studio.

The project question is:

How do pollution trends and pollutant patterns differ across five major global cities over time?

This is not a global leaderboard project. It is a focused five-city observatory.

## 2. Why This Is A Good Data Engineering Project

A strong data engineering project usually answers four questions:

1. Where does the data come from?
2. How does raw data move into storage?
3. How is raw data transformed into trusted analytical data?
4. How do users consume the final result?

This repo answers those questions with a clear batch pipeline:

```text
OpenAQ source data
-> Local Bronze landing in data/bronze
-> Spark Bronze to Silver transformation
-> Silver staged to GCS for BigQuery loading
-> BigQuery warehouse loading
-> dbt analytical marts
-> Looker Studio dashboard
```

## 3. Why These Five Cities

The project scope is fixed to:

- London
- New York
- Delhi
- Beijing
- Berlin

This smaller scope helps in four ways:

- it gives cross-region and policy contrast
- it creates strong analytical contrast
- it keeps the pipeline manageable
- it makes the dashboard readable during review

The single source of truth is [ingestion/location_targets.csv](../ingestion/location_targets.csv).

## 4. The Main Concepts You Need To Know

Before running anything, it helps to understand the pipeline vocabulary.

### Bronze

Bronze is the raw landing zone.

- data is downloaded from OpenAQ
- files are kept close to source format
- traceability matters more than analytics here

### Silver

Silver is the cleaned and standardized layer.

- Spark parses timestamps
- Spark standardizes pollutant names
- Spark filters to the fixed city scope
- Spark joins city metadata
- Spark removes duplicate rows
- Spark writes parquet output

### Warehouse

BigQuery stores curated analytical tables.

- one fact table for measurements
- supporting dimensions for cities and pollutants
- partitioned and clustered layout for better query performance

### Marts

dbt builds business-facing models for the dashboard.

- trend mart
- pollutant distribution mart
- cross-city comparison mart
- extreme events mart

## 5. Repository Tour

The main folders you will work with are:

- [ingestion/](../ingestion/) for source download and scope definition
- [spark/](../spark/) for Bronze to Silver transformation and Silver DQ
- [warehouse/](../warehouse/) for BigQuery loading
- [dbt/](../dbt/) for analytical marts
- [airflow/](../airflow/) for orchestration
- [docs/dashboard-design.md](dashboard-design.md) for dashboard structure
- [docs/](./) for reviewer-facing support docs

The main entry files are:

- [main.py](../main.py)
- [runbook.md](../runbook.md)
- [airflow/global_city_air_quality_observatory_dag.py](../airflow/global_city_air_quality_observatory_dag.py)

## 6. Local Setup From Scratch

### Step 1: Install the required tools

You need:

- Python `3.11` to `3.13`
- Java 17
- `uv`
- `gcloud`
- `bq`
- Terraform

### Step 2: Install Python dependencies

```bash
uv sync
```

### Step 3: Authenticate to GCP

```bash
gcloud auth login
gcloud auth application-default login
```

### Step 4: Prepare Terraform variables

```bash
cp terraform/terraform.tfvars.example terraform/terraform.tfvars
```

Edit the file with your real project values.

### Step 5: Provision cloud resources

```bash
cd terraform
terraform init
terraform plan -var-file=terraform.tfvars
terraform apply -var-file=terraform.tfvars
cd ..
```

## 7. Understanding The CLI Helpers

[main.py](../main.py) gives you three quick commands:

### Show the fixed project scope

```bash
uv run python main.py show-scope
```

This reads [ingestion/location_targets.csv](../ingestion/location_targets.csv) and prints the configured cities.

### Verify Bronze

```bash
uv run python main.py verify-bronze
```

This checks whether raw Bronze files and metadata exist.

### Verify the quality report

```bash
uv run python main.py verify-quality-report
```

This checks whether the Silver DQ report exists and whether it passed.

## 8. Running The Pipeline Manually

This is the best section to follow if you want to understand each stage deeply.

### Step 1: Show scope

```bash
uv run python main.py show-scope
```

Expected outcome:

- the five selected cities are printed

### Step 2: Download data into Bronze

```bash
uv run python ingestion/download_air_quality_data.py --mode backfill
```

Expected outcome:

- raw `csv.gz` files land in `data/bronze/`
- location metadata is written for the five-city scope

### Step 3: Verify Bronze

```bash
uv run python main.py verify-bronze
```

Expected outcome:

- Bronze file count is printed
- metadata file is confirmed

### Step 4: Run Spark Bronze to Silver

```bash
uv run python spark/bronze_to_silver.py --write-mode overwrite
```

Expected outcome:

- Spark reads raw files
- Spark writes partitioned parquet to `data/silver/air_quality_measurements/`
- Spark writes `data/silver/latest_run_summary.json`

### Step 5: Run Silver data quality checks

```bash
uv run python spark/check_silver_data_quality.py
```

Expected outcome:

- `data/quality/silver_dq_report.json` is created
- required columns, city scope, duplicates, and null checks are validated

### Step 6: Load BigQuery

```bash
uv run python warehouse/load_to_bigquery.py
```

Expected outcome:

- Silver parquet is staged to GCS
- BigQuery staging table is loaded
- warehouse fact and dimension tables are rebuilt

### Step 7: Run dbt

```bash
bash scripts/dbt_run.sh
```

Expected outcome:

- staging model runs
- reporting marts run

### Step 8: Test dbt

```bash
bash scripts/dbt_test.sh
```

Expected outcome:

- dbt tests pass

### Step 9: Verify the final quality report

```bash
uv run python main.py verify-quality-report
```

Expected outcome:

- final Silver DQ report is printed
- report status is `pass`

## 9. Running With Airflow

Airflow is the orchestration layer for the end-to-end batch flow.

The main DAG file is [airflow/global_city_air_quality_observatory_dag.py](../airflow/global_city_air_quality_observatory_dag.py).

The task flow is:

1. `show_scope`
2. `download_data`
3. `verify_bronze`
4. `bronze_to_silver`
5. `silver_data_quality`
6. `load_bigquery`
7. `dbt_run`
8. `dbt_test`
9. `verify_quality_report`

This DAG exists in two scheduling variants:

- `global_city_air_quality_backfill`
- `global_city_air_quality_daily`

## 10. Why Spark Is The Main Transformation Layer

Spark is the official Bronze to Silver engine in this repo.

Why Spark fits this project:

- many raw files must be read consistently
- a schema must be enforced
- timestamps must be parsed reliably
- pollutant names must be standardized
- duplicates must be removed
- output must be written as parquet for downstream loading

Pandas still appears in a few helper contexts such as local-quality checks and tests, but the main transformation story is Spark.

## 11. Why BigQuery Is Structured This Way

The warehouse fact table is optimized for dashboard access:

- partition by `measurement_date`
- cluster by `city`, `pollutant`

This matters because the dashboard commonly filters by:

- time
- city
- pollutant

That means the warehouse layout supports both performance and reviewer-facing design decisions.

## 12. What dbt Adds

dbt is not used for raw cleanup. Spark handles that earlier.

dbt adds value by:

- making analytical SQL models readable
- building reusable marts
- adding data tests
- supporting dashboard-ready outputs

The key marts are:

- `mart_city_pollution_trends`
- `mart_city_pollutant_distribution`
- `mart_city_comparison_summary`
- `mart_city_extreme_events`
- `mart_pm25_city_daily`

## 13. How To Think About The Dashboard

The dashboard should tell a five-city comparison story only.

Recommended pages:

### Page 1: City trend over time

- compare city trends over time

### Page 2: Pollutant distribution by city

- compare pollutant mix across the five cities

### Page 3: Cross-city comparison

- compare summary metrics side by side

### Page 4: Extreme events

- show notable spikes and outliers

## 14. What A Reviewer Will Look For

A reviewer will usually check:

- whether the project question is clear
- whether the city scope is consistent everywhere
- whether Spark is truly used for transformation
- whether Airflow orchestrates the full pipeline
- whether BigQuery is used as a warehouse
- whether dbt builds marts
- whether the dashboard matches the project question
- whether proof-of-run evidence exists

Useful supporting docs:

- [runbook.md](../runbook.md)
- [docs/review-guide.md](review-guide.md)
- [docs/architecture-decisions.md](architecture-decisions.md)
- [docs/execution-evidence.md](execution-evidence.md)

## 15. Common Problems And How To Debug Them

### Problem: `show-scope` prints nothing

Check:

- [ingestion/location_targets.csv](../ingestion/location_targets.csv) exists
- the file has five rows plus the header

### Problem: Bronze verification fails

Check:

- ingestion ran successfully
- `data/bronze/` contains `csv.gz` files
- `data/bronze/location_metadata.csv` exists

### Problem: Spark job returns zero rows

Check:

- Bronze files contain the configured location IDs
- metadata file matches the selected scope
- pollutant values are in the allowed set

### Problem: BigQuery load fails

Check:

- GCP auth is active
- bucket and dataset names are correct
- required APIs are enabled

### Problem: dbt fails

Check:

- `.venv-dbt` exists
- the dbt profile points to the correct GCP project and dataset
- the warehouse tables were successfully loaded

## 16. How To Produce Final Proof Of Run

The committed reviewer-facing evidence files live in [docs/images/](images/).

Current evidence assets include:

- `airflow_dag_graph.png`
- `airflow_success_run.png`
- `bronze_ingestion_success.png`
- `silver_quality_report.png`
- `load_to_bigquery.png`
- `bigquery_tables.png`
- `dbt_run_output.png`
- `dbt_test_output.png`
- `dashboard_overview.png`
- `Global_City_Air_Quality_Observatory_Dashboard.pdf`

They are described in [docs/execution-evidence.md](execution-evidence.md).

## 17. Suggested Learning Path

If you are new to data engineering, learn this project in this order:

1. Read [README.md](../README.md)
2. Read [docs/pipeline-overview.md](pipeline-overview.md)
3. Run `show-scope`
4. Run ingestion
5. Verify Bronze
6. Run Spark
7. Run Silver DQ
8. Load BigQuery
9. Run dbt
10. Study the dashboard
11. Run the Airflow DAG

## 18. Final Mental Model

If you remember only one sentence, remember this:

Global City Air Quality Observatory is a batch data engineering project that compares air pollution trends and pollutant patterns across London, New York, Delhi, Beijing, and Berlin using OpenAQ, GCP, Spark, BigQuery, dbt, Airflow, and Looker Studio.
