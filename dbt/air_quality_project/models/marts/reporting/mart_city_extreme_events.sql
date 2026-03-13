with ranked_events as (
    select
      measurement_datetime,
      measurement_date,
      city,
      country,
      location_name,
      pollutant,
      measurement_value,
      measurement_unit,
      row_number() over (
        partition by city, pollutant
        order by measurement_value desc, measurement_datetime desc
      ) as city_pollutant_rank
    from {{ ref('stg_air_quality') }}
)

select
  measurement_datetime,
  measurement_date,
  city,
  country,
  location_name,
  pollutant,
  measurement_value,
  measurement_unit,
  city_pollutant_rank
from ranked_events
where city_pollutant_rank <= 10
