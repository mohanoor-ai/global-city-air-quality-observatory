# Dashboard Design

This dashboard compares air pollution across five selected cities:
London, New York, Delhi, Beijing, and Berlin.

## Main dashboard pages

### 1. City trend over time

Shows pollutant measurements over time for each city.

### 2. Pollutant distribution by city

Shows the relative distribution of pollutants within each city.

### 3. Cross-city comparison

Compares pollution measurements across the five cities.

### 4. Extreme events

Highlights unusually high pollution readings within the selected five-city scope.

## Style guide

Use a clean, readable layout that supports the five-city comparison story.

### Colors

- background: `#F7F9FC`
- card background: `#FFFFFF`
- primary text: `#1F2937`
- secondary text: `#6B7280`

Pollutants:

- `pm25`: `#D14343`
- `pm10`: `#F08A24`
- `no2`: `#3A86FF`
- `co`: `#2A9D8F`
- `o3`: `#6C5CE7`

## Layout suggestion

1. Top filters: date, pollutant, city
2. City trend over time chart
3. Pollutant distribution by city chart
4. Optional city scorecard
5. Optional extreme events table

## Chart rules

- Keep pollutant legend order consistent: `pm25`, `pm10`, `no2`, `co`, `o3`
- Use consistent y-axis label: `Pollution Value`
- Prefer clear labels over dense styling
