-- Mart-level validation queries

-- 1) Row counts per mart
SELECT 'mart_pm25_by_country' AS mart_name, COUNT(*) AS row_count
FROM `aq-pipeline-260309-5800.air_quality_dbt_marts.mart_pm25_by_country`
UNION ALL
SELECT 'mart_pm25_by_city', COUNT(*)
FROM `aq-pipeline-260309-5800.air_quality_dbt_marts.mart_pm25_by_city`
UNION ALL
SELECT 'mart_pollution_trends', COUNT(*)
FROM `aq-pipeline-260309-5800.air_quality_dbt_marts.mart_pollution_trends`
UNION ALL
SELECT 'mart_pollutant_distribution', COUNT(*)
FROM `aq-pipeline-260309-5800.air_quality_dbt_marts.mart_pollutant_distribution`
UNION ALL
SELECT 'mart_extreme_pollution_events', COUNT(*)
FROM `aq-pipeline-260309-5800.air_quality_dbt_marts.mart_extreme_pollution_events`;

-- 2) Duplicate grain check: mart_pm25_by_country
SELECT month_start, country, COUNT(*) AS row_count
FROM `aq-pipeline-260309-5800.air_quality_dbt_marts.mart_pm25_by_country`
GROUP BY month_start, country
HAVING COUNT(*) > 1;

-- 3) Duplicate grain check: mart_pm25_by_city
SELECT month_start, country, city, COUNT(*) AS row_count
FROM `aq-pipeline-260309-5800.air_quality_dbt_marts.mart_pm25_by_city`
GROUP BY month_start, country, city
HAVING COUNT(*) > 1;
