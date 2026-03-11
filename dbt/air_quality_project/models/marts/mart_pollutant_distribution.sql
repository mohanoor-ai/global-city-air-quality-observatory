select
  country,
  city,
  pollutant,
  count(*) as measurement_count,
  round(avg(value), 3) as avg_value,
  approx_quantiles(value, 100)[offset(50)] as median_value,
  approx_quantiles(value, 100)[offset(95)] as p95_value,
  max(value) as max_value
from {{ ref('stg_air_quality') }}
group by 1, 2, 3
