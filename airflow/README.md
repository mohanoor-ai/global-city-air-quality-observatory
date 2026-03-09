# Airflow DAGs

This folder contains Airflow orchestration for the pipeline.

---

## DAG Included

- `air_quality_pipeline_dag`
  - `build_silver`
  - `data_quality_gate`
  - `load_warehouse`

Task order:

`build_silver -> data_quality_gate -> load_warehouse`

---

## Local Run (Quick Start)

From the project root:

```bash
uv sync
uv run python processing/clean_air_quality_data.py
uv run python processing/check_silver_data_quality.py
uv run python warehouse/load_to_bigquery.py
```

This runs the same steps the DAG orchestrates.

---

## Airflow Notes

- DAG file: `airflow/air_quality_pipeline_dag.py`
- Project root used by DAG: `/home/moha_/projects/air-quality-data-pipeline`
- Schedule: `@daily`
- Catchup: `False`
