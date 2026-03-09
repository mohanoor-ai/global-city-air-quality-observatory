select
  measurement_date,
  pollutant,
  round(avg(value), 3) as avg_pollution_value,
  count(*) as measurement_count
from {{ ref('stg_air_quality') }}
group by 1, 2
