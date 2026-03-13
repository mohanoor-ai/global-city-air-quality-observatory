# Proof Of Run

Store reviewer-facing proof-of-run screenshots in [docs/images/](images/).

Required screenshots:

- Terraform apply success: [docs/images/terraform-apply.png](images/terraform-apply.png)
- Airflow DAG success: [docs/images/airflow-success.png](images/airflow-success.png)
- Bronze files in GCS: [docs/images/gcs-bronze-files.png](images/gcs-bronze-files.png)
- Silver parquet output: [docs/images/silver-parquet-output.png](images/silver-parquet-output.png)
- BigQuery tables created: [docs/images/bigquery-tables.png](images/bigquery-tables.png)
- dbt run success: [docs/images/dbt-run.png](images/dbt-run.png)
- dbt test success: [docs/images/dbt-test.png](images/dbt-test.png)
- Looker Studio dashboard: [docs/images/dashboard.png](images/dashboard.png)

Suggested capture order:

1. Terraform apply success
2. Bronze files visible in GCS
3. Silver parquet output visible after Spark
4. Airflow DAG success
5. BigQuery tables created
6. dbt run success
7. dbt test success
8. Looker Studio dashboard

Optional supporting artifacts:

- terminal output from `uv run python spark/check_silver_data_quality.py`
- terminal output from `uv run python -m unittest -v tests/test_pipeline_checks.py`
- exported JSON from `data/quality/silver_dq_report.json`
