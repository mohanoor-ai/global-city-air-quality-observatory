select
  date_trunc(measurement_date, month) as month_start,
  pollutant,
  round(avg(value), 3) as avg_value,
  max(value) as max_value,
  count(*) as measurement_count
from {{ ref('stg_air_quality') }}
group by 1, 2
