select
  measurement_date,
  city,
  country,
  pollutant,
  round(avg(measurement_value), 3) as avg_measurement_value,
  max(measurement_value) as max_measurement_value,
  count(*) as measurement_count
from {{ ref('stg_air_quality') }}
group by 1, 2, 3, 4
