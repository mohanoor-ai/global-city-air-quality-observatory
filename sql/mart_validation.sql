-- Mart-level validation queries

-- 1) Row counts per mart
SELECT 'mart_pm25_city_daily' AS mart_name, COUNT(*) AS row_count
FROM `aq-pipeline-260309-5800.air_quality_dbt_marts.mart_pm25_city_daily`
UNION ALL
SELECT 'mart_city_pollution_trends', COUNT(*)
FROM `aq-pipeline-260309-5800.air_quality_dbt_marts.mart_city_pollution_trends`
UNION ALL
SELECT 'mart_city_pollutant_distribution', COUNT(*)
FROM `aq-pipeline-260309-5800.air_quality_dbt_marts.mart_city_pollutant_distribution`
UNION ALL
SELECT 'mart_city_extreme_events', COUNT(*)
FROM `aq-pipeline-260309-5800.air_quality_dbt_marts.mart_city_extreme_events`
UNION ALL
SELECT 'mart_city_comparison_summary', COUNT(*)
FROM `aq-pipeline-260309-5800.air_quality_dbt_marts.mart_city_comparison_summary`;

-- 2) Duplicate grain check: mart_pm25_city_daily
SELECT measurement_date, city, COUNT(*) AS row_count
FROM `aq-pipeline-260309-5800.air_quality_dbt_marts.mart_pm25_city_daily`
GROUP BY measurement_date, city
HAVING COUNT(*) > 1;

-- 3) Duplicate grain check: mart_city_pollutant_distribution
SELECT city, pollutant, COUNT(*) AS row_count
FROM `aq-pipeline-260309-5800.air_quality_dbt_marts.mart_city_pollutant_distribution`
GROUP BY city, pollutant
HAVING COUNT(*) > 1;
