select
  city,
  country,
  avg_pm25,
  avg_pm10,
  avg_no2,
  measurement_count
from {{ ref('mart_city_comparison_summary') }}
where coalesce(avg_pm25, avg_pm10, avg_no2) is null
