Default to the simplest defensible implementation.

# AGENTS.md

## Project identity

This repository is an air quality analytics project.

The goal is to make this repository look like a strong, believable, human-built final project.

It must **not** look like an over-engineered AI-generated codebase.
It must look like a careful builder created it, understands it, and can explain every major choice.

## Locked project direction

### Project theme
Air quality analytics pipeline using historical air quality data.

### Data strategy
- historical backfill for the **last 2 full years plus current year-to-date**
- daily incremental ingestion after backfill

### Main project question
Which countries and cities have the worst PM2.5 exposure over time, and where are trends improving or worsening?

### Dashboard story
1. Global trend  
   How pollution changes over time

2. Worst countries  
   Which countries have the highest average PM2.5

3. Worst cities  
   Which cities have the highest average PM2.5

4. Pollutant comparison  
   How major pollutants compare across locations

### Core metrics
- average PM2.5 by country
- average PM2.5 by city
- monthly PM2.5 trend over time
- highest recorded pollutant value by location
- pollutant distribution by type

### Final mart tables
- `mart_pm25_by_country`
- `mart_pm25_by_city`
- `mart_pollution_trends`
- `mart_pollutant_distribution`
- `mart_extreme_pollution_events`

## Primary goal

Make the repository consistent with this locked direction.

Everything in the repo should support this exact story.
Do not leave broad, generic, or over-claimed wording.
Do not build random extra features outside this scope.

## Code style rules

Code must feel like practical human work:
- simple
- readable
- modest
- easy to explain
- not too clever
- not too abstract

Prefer:
- plain Python
- direct control flow
- small functions
- obvious naming
- light modularity only where helpful

Avoid:
- unnecessary classes
- deep abstractions
- factory patterns
- registries
- plugin architectures
- complex config systems
- unnecessary helper layers
- generic framework-style code
- enterprise-style wording
- “production-grade” claims unless truly proven

Important:
- default to the simplest defensible implementation
- preserve working functionality
- do not rewrite everything without reason
- make minimal, high-confidence changes
- if something is unfinished, represent it honestly

## Documentation rules

Documentation must sound natural and project-owned.

Requirements:
- be precise
- be honest
- remove over-claiming
- clearly separate:
  - implemented now
  - partially implemented
  - planned next

Do not use inflated wording like:
- enterprise-ready
- highly scalable
- production-grade
- robust platform

unless there is clear evidence for it.

README must match the actual repo exactly.

## What must be true after changes

A reviewer should be able to open the repo and quickly understand:
- what data period is used
- what the historical backfill does
- what the daily incremental pipeline does
- how raw data becomes cleaned data
- how cleaned data is loaded to the warehouse
- how marts answer the main project question
- how the dashboard uses the marts
- how the project maps to the documented architecture and outputs

## Repository tasks

### 1. Audit the repo
Inspect the existing repo carefully and identify:
- over-claimed features
- inconsistent docs
- generic AI-sounding text
- code that feels too polished or too abstract
- places where implementation and README do not match
- any one-location or one-year assumptions that conflict with the locked direction

### 2. Fix README first
Rewrite the README so it is aligned to the locked project.

The README should include:
- project overview
- locked main question
- data strategy
- historical backfill vs daily incremental
- architecture overview
- medallion/layer flow if used
- final mart tables
- dashboard story
- implementation mapping
- implemented now
- planned next
- limitations

Important:
- narrow scope if needed to stay believable
- do not claim anything not present in code or clearly marked as planned

### 3. Align ingestion to the new data strategy
Refactor or simplify ingestion so it clearly supports:
- one historical backfill mode
- one daily incremental mode

Requirements:
- backfill loads the selected time range: last 2 full years + current year-to-date
- daily mode ingests only the newest available slice
- code should be simple and easy to explain
- avoid unnecessary orchestration complexity inside scripts
- if exact daily ingestion cannot be fully completed, leave a simple honest TODO rather than faking completeness

### 4. Ensure multi-country / multi-city support
The project question is now about countries and cities.

Requirements:
- remove assumptions that the project is only one city or one location unless explicitly marked as a temporary limitation
- transformations should preserve the fields needed for:
  - country-level analysis
  - city-level analysis
  - pollutant-level analysis
  - time trends

### 5. Make PM2.5 the main analytical focus
The project revolves around PM2.5.

Requirements:
- PM2.5 should be clearly prioritized in docs, marts, and examples
- other pollutants can still be included for comparison and distribution
- naming and descriptions should reflect this

### 6. Build or clean up marts
Create or refactor marts so they directly support the final metrics.

Target marts:
- `mart_pm25_by_country`
- `mart_pm25_by_city`
- `mart_pollution_trends`
- `mart_pollutant_distribution`
- `mart_extreme_pollution_events`

Requirements:
- keep model logic simple and readable
- use clear grain
- use obvious column names
- avoid over-modeling
- if dbt is used, keep the dbt project simple and understandable
- if dbt is not yet fully implemented, document that honestly

Suggested purposes:
- `mart_pm25_by_country`: country-level PM2.5 averages
- `mart_pm25_by_city`: city-level PM2.5 averages
- `mart_pollution_trends`: monthly pollution trends over time
- `mart_pollutant_distribution`: pollutant distribution and comparison
- `mart_extreme_pollution_events`: highest observed pollution values

### 7. Keep orchestration modest
If orchestration exists or is added:
- keep it simple
- the workflow should be easy to explain
- do not add advanced scheduling patterns unless clearly needed

The workflow should reflect:
- backfill pipeline
- daily incremental pipeline

If orchestration is not fully implemented:
- document the intended workflow honestly
- do not fake a completed orchestration layer

### 8. Testing
Add only sensible, lightweight tests.
Do not create a huge testing framework.

Good targets:
- unit tests for transformation logic
- simple validation for expected columns
- tests for marts if appropriate
- dbt tests if dbt is implemented

### 9. Improve ownership feel
Make the repo feel clearly owned by the project author.

This means:
- comments should sound natural
- naming should be domain-specific
- docs should explain trade-offs simply
- choices should be justified in plain language
- avoid generic template text

## Working style

As you work:
- inspect before changing
- prefer minimal edits over massive rewrites
- keep functionality intact
- simplify where possible
- make the repo internally consistent

When you find problems:
- fix them directly where possible
- if something cannot be fully implemented now, leave a clear modest note
- do not leave grand placeholders

Do not add complexity just to look impressive.

A reviewer should think:
“This project is coherent and intentionally built.”

## Quality bar

Final result should be:
- focused
- coherent
- honest
- simple
- defensible
- clearly mapped to the documented project goals

Every major file and design choice should be explainable in a project review.
