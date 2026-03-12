# Docs Index

This folder keeps short project notes that match the current implementation.

## Core docs

- `data-source.md`: OpenAQ archive source and file pattern used by ingestion
- `pipeline-overview.md`: high-level flow from Bronze to marts
- `pipeline-orchestration.md`: Airflow DAG entrypoints and task chain
- `data-lake-design.md`: local and cloud storage layout (`bronze` and `silver`)
- `analytics-and-metrics.md`: dashboard question, metrics, and mart mapping
- `architecture-decisions.md`: small set of decisions and trade-offs
- `infrastructure.md`: what Terraform creates and what still needs manual setup
- `repository-structure.md`: quick folder map
- `environment-setup.md` and `local-setup.md`: tooling and local commands
- `custom-location-testing.md`: how to run ingestion/pipeline with any custom city/location ID list
- `project-plan.md`: finalized project scope summary
- `review-guide.md`: 5-minute walkthrough for markers
- `submission-notes.md`: final delivered scope summary

If a doc conflicts with `README.md`, treat `README.md` as the source of truth and update the doc.
