select
  city,
  country,
  pollutant,
  round(avg(measurement_value), 3) as avg_measurement_value,
  approx_quantiles(measurement_value, 100)[offset(50)] as median_measurement_value,
  approx_quantiles(measurement_value, 100)[offset(95)] as p95_measurement_value,
  count(*) as measurement_count
from {{ ref('stg_air_quality') }}
group by 1, 2, 3
