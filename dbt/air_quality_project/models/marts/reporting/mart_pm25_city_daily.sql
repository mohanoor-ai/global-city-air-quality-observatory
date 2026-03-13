select
  measurement_date,
  city,
  country,
  round(avg(measurement_value), 3) as avg_pm25,
  max(measurement_value) as max_pm25,
  count(*) as measurement_count
from {{ ref('stg_air_quality') }}
where pollutant = 'pm25'
group by 1, 2, 3
