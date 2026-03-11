select
  date_trunc(measurement_date, month) as month_start,
  country,
  city,
  round(avg(value), 3) as avg_pm25,
  max(value) as max_pm25,
  count(*) as measurement_count
from {{ ref('stg_air_quality') }}
where pollutant = 'pm25'
group by 1, 2, 3
