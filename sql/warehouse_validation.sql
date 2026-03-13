-- Warehouse-level validation queries

-- 1) Base row count
SELECT COUNT(*) AS total_rows
FROM `aq-pipeline-260309-5800.air_quality_dw.fct_air_quality_measurements`;

-- 2) Null checks on key fields
SELECT
  COUNTIF(measurement_datetime IS NULL) AS null_measurement_datetime,
  COUNTIF(measurement_date IS NULL) AS null_measurement_date,
  COUNTIF(city IS NULL) AS null_city,
  COUNTIF(location_id IS NULL) AS null_location_id,
  COUNTIF(pollutant IS NULL) AS null_pollutant,
  COUNTIF(measurement_value IS NULL) AS null_measurement_value
FROM `aq-pipeline-260309-5800.air_quality_dw.fct_air_quality_measurements`;

-- 3) Pollutant distribution
SELECT pollutant, COUNT(*) AS measurement_count
FROM `aq-pipeline-260309-5800.air_quality_dw.fct_air_quality_measurements`
GROUP BY pollutant
ORDER BY measurement_count DESC;
