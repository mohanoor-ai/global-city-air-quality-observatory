select
  measurement_datetime,
  date(measurement_datetime) as measurement_date,
  location_id,
  location_name,
  coalesce(nullif(trim(city), ''), 'unknown') as city,
  coalesce(nullif(trim(upper(country)), ''), 'UNKNOWN') as country,
  latitude,
  longitude,
  lower(pollutant) as pollutant,
  cast(value as float64) as value,
  unit
from {{ source('warehouse', 'air_quality_measurements') }}
