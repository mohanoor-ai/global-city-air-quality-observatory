select
  city,
  country,
  round(avg(case when pollutant = 'pm25' then measurement_value end), 3) as avg_pm25,
  round(avg(case when pollutant = 'pm10' then measurement_value end), 3) as avg_pm10,
  round(avg(case when pollutant = 'no2' then measurement_value end), 3) as avg_no2,
  max(measurement_date) as latest_measurement_date,
  count(*) as measurement_count
from {{ ref('stg_air_quality') }}
group by 1, 2
