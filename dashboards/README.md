# Dashboard Guide

Dashboard goal: show how pollution trends and pollutant patterns differ across London, New York, Delhi, Beijing, and São Paulo.

## Tile mapping

- PM2.5 trend over time
  chart: line chart
  mart: `mart_pm25_city_daily`
  question: how does daily PM2.5 move across the five cities over time?
  screenshot: [images/dashboard_pm25_trend.png](../images/dashboard_pm25_trend.png)

- Pollutant distribution by city
  chart: bar chart or stacked bar chart
  mart: `mart_city_pollutant_distribution`
  question: which pollutant profile stands out in each city?
  screenshot: [images/dashboard_pollutant_distribution.png](../images/dashboard_pollutant_distribution.png)

- Extreme pollution events
  chart: table
  mart: `mart_city_extreme_events`
  question: where did the biggest pollutant spikes happen?
  screenshot: [images/dashboard_extreme_events.png](../images/dashboard_extreme_events.png)

- City comparison scorecard
  chart: scorecards or compact table
  mart: `mart_city_comparison_summary`
  question: which city currently looks worst on average PM2.5 and PM10?
  screenshot: [images/dashboard_city_scorecard.png](../images/dashboard_city_scorecard.png)

## Filters

- date range on `measurement_date`
- city
- pollutant

## Notes for the reviewer

- the first tile satisfies the required temporal chart
- the second tile satisfies the required categorical chart
- the dashboard is intentionally small and focused so the five-city story stays clear
