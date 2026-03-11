# Submission Notes

## Implemented now

- OpenAQ ingestion supports:
  - historical backfill (`last 2 full years + current year-to-date`)
  - daily incremental (`latest file per configured location`)
- Global starter location coverage (one major city per inhabited continent)
- Bronze -> Silver cleaning with PM2.5-focused pollutant set
- Silver quality checks with JSON reporting
- BigQuery load script and dbt marts aligned to dashboard story
- Simple Airflow DAGs for backfill and daily runs

## Partial

- Dashboard screenshots are not yet complete in `images/`.
- Cloud execution evidence (fresh row counts / dbt test logs for the updated 6-city scope) is still pending.

## Limitations

- Country and city comparisons depend on configured target locations, not every monitoring station worldwide.
- `mart_pollution_trends` includes all selected pollutants for comparison; PM2.5-specific trends come from filtering pollutant = `pm25`.
- Infrastructure is intentionally minimal and not a full production deployment.

## Next steps

- Run one clean end-to-end cloud pass with updated targets and record validation outputs in `runbook.md`.
- Add dashboard screenshots for each section in `images/`.
- Add one more city per continent for broader comparisons while keeping runtime manageable.
