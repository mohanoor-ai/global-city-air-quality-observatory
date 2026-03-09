select
  measurement_datetime,
  date(measurement_datetime) as measurement_date,
  location_name,
  latitude,
  longitude,
  lower(pollutant) as pollutant,
  cast(value as float64) as value,
  unit
from {{ source('warehouse', 'air_quality_measurements') }}
