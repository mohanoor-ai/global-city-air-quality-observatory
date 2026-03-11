with ranked_events as (
    select
      measurement_datetime,
      measurement_date,
      country,
      city,
      location_name,
      pollutant,
      value,
      unit,
      row_number() over (
        partition by pollutant
        order by value desc, measurement_datetime desc
      ) as pollutant_rank
    from {{ ref('stg_air_quality') }}
)

select
  measurement_datetime,
  measurement_date,
  country,
  city,
  location_name,
  pollutant,
  value,
  unit,
  pollutant_rank
from ranked_events
where pollutant_rank <= 100
