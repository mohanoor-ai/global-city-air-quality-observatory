# Submission Notes

## Final Scope

- OpenAQ ingestion supports:
  - historical backfill (`last 2 full years + current year-to-date`)
  - daily incremental (`latest file per configured location`)
- Global starter location coverage (one major city per inhabited continent)
- Bronze -> Silver cleaning with PM2.5-focused pollutant set
- Silver quality checks with JSON reporting
- BigQuery load script and dbt marts aligned to dashboard story
- Simple Airflow DAGs for backfill and daily runs
- Dashboard screenshot file structure in `images/`
- Validation SQL files in `sql/` for warehouse and marts
