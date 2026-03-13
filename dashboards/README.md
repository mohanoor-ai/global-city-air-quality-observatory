# Dashboard Guide

This dashboard compares London, New York, Delhi, Beijing, and São Paulo through a focused five-city analytics story.

The goal is not to rank every country or city in the world. The goal is to compare how pollution trends and pollutant patterns differ across the fixed capstone scope.

## Page 1: City Trend Over Time

- Purpose: show how pollution changes over time for the five selected cities
- Main view: time-series trend chart by city
- Recommended mart: `mart_city_pollution_trends`
- Reviewer takeaway: city trajectories differ over time and should be compared directly, not through global ranking tables

## Page 2: Pollutant Distribution By City

- Purpose: compare pollutant mix and concentration profile across the five cities
- Main view: grouped bar chart, stacked bar chart, or heatmap by city and pollutant
- Recommended mart: `mart_city_pollutant_distribution`
- Reviewer takeaway: each city has a different pollutant profile, not just a different overall level

## Page 3: Cross-City Comparison

- Purpose: give a compact comparison of the five cities on the same dashboard page
- Main view: scorecards or comparison table
- Recommended mart: `mart_city_comparison_summary`
- Reviewer takeaway: the dashboard supports quick cross-city comparison without expanding into a global leaderboard

## Page 4: Extreme Events

- Purpose: surface unusual spikes and notable pollution events inside the selected city scope
- Main view: ranked table or filtered event view
- Recommended mart: `mart_city_extreme_events`
- Reviewer takeaway: city averages alone do not show the most severe local events

## Filters

- date range
- city
- pollutant

## Reviewer Notes

- The dashboard is intentionally limited to five cities to keep the story readable and defensible.
- The dashboard should show both a temporal comparison and a categorical comparison.
- Screenshot evidence should be stored under [docs/images/](../docs/images/).
