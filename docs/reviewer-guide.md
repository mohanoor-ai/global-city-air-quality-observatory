# Reviewer Guide

## Likely viva questions

Why these five cities?

- They give global spread, strong analytical contrast, practical source coverage, and a readable dashboard scope.

Why batch instead of streaming?

- The source arrives as archive files, and the project rubric only needs one end-to-end approach. Batch matches the source and is simpler to operate.

Why Spark instead of Pandas?

- The Silver layer now handles many files, schema enforcement, timestamp parsing, pollutant standardization, metadata joins, deduplication, and partitioned parquet output.

What is the grain of Silver?

- One row per city, station, timestamp, and pollutant measurement.

What is the grain of the fact table?

- One row per city, station, timestamp, and pollutant measurement after Silver standardization and BigQuery typing.

Why partition by date and cluster by city and pollutant?

- Time, city, and pollutant are the three main dashboard filters and the main drivers of query cost.

What transformations happen in Spark versus dbt?

- Spark does raw-file cleanup and standardization.
- dbt does analytical modeling for trend, distribution, extreme event, and scorecard marts.

What are the main dashboard insights?

- daily PM2.5 trends differ sharply across the five cities
- pollutant mixes are not the same across cities
- extreme-event tiles help show spikes that averages hide

What happens when metadata is missing?

- The ingestion scope writes explicit city metadata, and the Spark join uses that controlled mapping before warehouse load.

How would a sixth city be added?

- Add a new scoped location to [ingestion/location_targets.csv](/home/moha_/projects/air-quality-data-pipeline/ingestion/location_targets.csv), update [ingestion/city_scope.py](/home/moha_/projects/air-quality-data-pipeline/ingestion/city_scope.py), rerun ingestion, Spark, warehouse load, and dbt.
