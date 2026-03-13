select
  city,
  country,
  measurement_datetime,
  measurement_date,
  location_id,
  location_name,
  sensor_id,
  latitude,
  longitude,
  lower(pollutant) as pollutant,
  cast(measurement_value as float64) as measurement_value,
  measurement_unit,
  batch_date,
  source_file
from {{ source('warehouse', 'fct_air_quality_measurements') }}
