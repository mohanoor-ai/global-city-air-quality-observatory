# Lessons Learned

- I narrowed the scope to five cities because the earlier version looked broad but weak. The smaller scope made the dashboard and README much easier to defend.
- Spark replaced Pandas because the Silver layer stopped being a simple cleanup step. Once I needed schema enforcement, timestamp normalization, metadata joins, deduplication, and partitioned parquet output, Spark was a better fit.
- I chose batch over streaming because the OpenAQ archive is naturally file-based and the rubric only needs one clear end-to-end pattern done well.
- The biggest data-quality issue was inconsistent pollutant naming and missing city metadata at the raw file level. I solved that by standardizing pollutants and joining explicit scope metadata before the warehouse load.
- BigQuery partitioning and clustering mattered more than I expected. The dashboard always filters by time, city, and pollutant, so the warehouse layout should match that.
- If I extended this project, I would add a clearer station dimension, unit harmonization rules, and an automated merge strategy for daily loads instead of recreating the fact table.
