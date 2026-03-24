# Reviewer guide

This document is the fastest way to inspect the project. It links the core code,
evidence, and run instructions a reviewer can use to judge the repository in a
few minutes without running the full pipeline.

---

## What this project does in one sentence

A batch pipeline that downloads OpenAQ archive data for five cities, transforms
it from Bronze to Silver, stages curated parquet data in GCS, loads it into
BigQuery, builds dbt marts, and presents the results in a Looker Studio
dashboard.

---

## 5-step reviewer walkthrough

### Step 1 - Understand the pipeline

Start with the architecture section in the root README. The project flow is:

```text
OpenAQ source data
-> Local Bronze landing in data/bronze
-> Spark Bronze to Silver transformation
-> Silver staged to GCS for BigQuery loading
-> BigQuery warehouse loading
-> dbt analytical marts
-> Looker Studio dashboard
```

Architecture decisions and tradeoffs are documented in
[`docs/architecture-decisions.md`](architecture-decisions.md).

---

### Step 2 - Verify the code exists

| Component | File |
|---|---|
| Ingestion | `ingestion/download_air_quality_data.py` |
| City scope config | `ingestion/location_targets.csv` |
| Spark transform | `spark/bronze_to_silver.py` |
| Silver quality checks | `spark/check_silver_data_quality.py` |
| BigQuery loader | `warehouse/load_to_bigquery.py` |
| Airflow DAGs | `airflow/global_city_air_quality_observatory_dag.py` |
| dbt staging | `dbt/air_quality_project/models/staging/stg_air_quality.sql` |
| dbt marts | `dbt/air_quality_project/models/marts/reporting/` |
| Terraform IaC | `terraform/main.tf`, `terraform/variables.tf`, `terraform/versions.tf` |

---

### Step 3 - Check proof of run

Proof-of-run screenshots and committed artifacts are collected in
[`docs/execution-evidence.md`](execution-evidence.md).

Evidence currently committed includes:

- Airflow DAG graph and successful run screenshots
- Bronze ingestion terminal output
- Silver data quality screenshot and committed JSON report values
- BigQuery load output
- BigQuery tables screenshot
- dbt run output
- dbt test output and parsed test summary
- Dashboard screenshot and PDF export

The remaining evidence gap is a committed GCS Silver staging screenshot. The
exact capture command is documented in `docs/execution-evidence.md`.

---

### Step 4 - View the dashboard

Live dashboard:
[Global City Air Quality Observatory - Looker Studio](https://lookerstudio.google.com/reporting/6432e2e1-4363-493c-bbf8-598c60bb49de)

If the live link is unavailable or still restricted by Google sharing settings,
use the committed PDF export:

- `docs/images/Global_City_Air_Quality_Observatory_Dashboard.pdf`

---

### Step 5 - Verify reproducibility

Full setup and run instructions live in [`runbook.md`](../runbook.md).

Quick reproducibility checks:

- `pyproject.toml` and `uv.lock` pin the Python environment
- `terraform/terraform.tfvars.example` shows the expected Terraform inputs
- `scripts/airflow_standalone.sh` starts local Airflow from a dedicated env
- `scripts/dbt_run.sh` and `scripts/dbt_test.sh` wrap dbt execution
- `main.py` provides the scope and verification CLI commands
- `Makefile` provides one-command targets for setup, infra, pipeline runs, and tests

---

## What you can verify without running anything

| Claim | Where to verify |
|---|---|
| Pipeline is end to end | `README.md` architecture section plus this guide |
| Terraform provisions storage and warehouse resources | `terraform/main.tf` |
| Airflow covers the full 9-task flow | `airflow/global_city_air_quality_observatory_dag.py` |
| Fact table is partitioned and clustered | `terraform/main.tf`, `warehouse/load_to_bigquery.py` |
| dbt marts are non-trivial aggregations | `dbt/air_quality_project/models/marts/reporting/` |
| Pipeline has committed run evidence | `docs/execution-evidence.md` and `docs/images/` |
| Dashboard exists with multiple chart types | `docs/dashboard-design.md`, `docs/images/dashboard_overview.png`, live link above |

---

## Known limitations

- Airflow is configured for local execution rather than Docker Compose deployment
- GCP credentials and a populated `terraform/terraform.tfvars` file are still required to run cloud steps
- The committed evidence set is strong, but the GCS Silver bucket screenshot still needs to be captured and added
- Dashboard access depends on the current Looker Studio sharing settings; the PDF export is the fallback
