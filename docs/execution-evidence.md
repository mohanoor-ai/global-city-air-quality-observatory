# Execution Evidence

This file is the checklist for proof-of-run artifacts.

Store screenshots or pasted outputs for:

- Airflow DAG success: [images/airflow_backfill_success.png](../images/airflow_backfill_success.png)
- BigQuery tables: [images/bigquery_tables.png](../images/bigquery_tables.png)
- dbt run and test output: [images/dbt_run_output.png](../images/dbt_run_output.png)
- dashboard: [images/dashboard_pm25_trend.png](../images/dashboard_pm25_trend.png)
- Terraform apply summary: [images/terraform_apply_summary.png](../images/terraform_apply_summary.png)
- Spark job output: [images/spark_job_output.png](../images/spark_job_output.png)

Local validation already available in this repo:

- unit test coverage for ingestion scope, Silver quality checks, and comparison logic
- Spark run summary at `data/silver/latest_run_summary.json`
- Silver DQ report at `data/quality/silver_dq_report.json`

Most recent local validation command run during this refactor:

```bash
uv run python -m unittest -v tests/test_pipeline_checks.py
```

Result:

- 9 tests passed
- covered city scope validation, ingestion helper logic, Silver DQ checks, and city comparison metrics

Cloud-side screenshots still need to be captured from a live GCP run because this refactor was completed without access to Airflow UI, BigQuery UI, Terraform apply output, or Looker Studio in this environment.

Recommended evidence capture order:

1. Save the Terraform apply summary.
2. Save one Spark job success log and the Silver DQ report.
3. Save the Airflow graph or grid view showing the full DAG succeeded.
4. Save the BigQuery table list and one partitioned fact-table details view.
5. Save the Looker Studio dashboard with the PM2.5 trend tile and pollutant distribution tile visible.
