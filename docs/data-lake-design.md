# Data Lake Design

This document defines how raw and processed data will be stored in the data lake.

The data lake will store files before they are loaded into the data warehouse.

The goal is to keep the storage structure simple, organized, and easy to query.

---

# Storage Location

The data lake will be stored in **Google Cloud Storage (GCS)**.

Example bucket:

```text
gs://air-quality-data-lake
Data Lake Layers

The data lake will contain two main layers.

Raw Layer

The raw layer stores data as close as possible to the source.

Characteristics:

minimal transformation

original schema preserved

used as the source of truth

Example path:

raw/openaq/

Example structure:

raw/openaq/year=YYYY/month=MM/

Example file:

raw/openaq/year=2024/month=01/air_quality.parquet
Curated Layer

The curated layer contains cleaned and structured data.

Characteristics:

cleaned schema

consistent column naming

ready for warehouse loading

Example path:

curated/air_quality/

Example structure:

curated/air_quality/year=YYYY/month=MM/

Example file:

curated/air_quality/year=2024/month=01/air_quality_clean.parquet
File Format

The data lake will use Parquet format.

Reasons:

columnar storage

efficient compression

faster query performance

good integration with BigQuery

widely used in modern data engineering pipelines

Partition Strategy

Files will be partitioned by time.

Example partitions:

year=YYYY
month=MM

Example directory structure:

year=2024/month=01/
year=2024/month=02/
year=2024/month=03/

This allows efficient filtering and querying.

Naming Conventions

File naming should remain simple and consistent.

Example raw file:

air_quality_raw.parquet

Example curated file:

air_quality_clean.parquet
Data Flow

The expected data flow is:

OpenAQ
→ Python ingestion
→ Raw Parquet files
→ Upload to GCS raw layer
→ Cleaning and transformation
→ Curated Parquet files
→ Load into BigQuery

BigQuery Integration

BigQuery will load data from the curated layer.

This can be done using:

batch load jobs

scheduled loads

Airflow tasks

Example load path:

gs://air-quality-data-lake/curated/air_quality/year=*/month=*/*.parquet
Benefits of This Design

This data lake structure provides:

clear separation of raw and cleaned data

reproducible pipelines

efficient partitioning

easy warehouse loading

scalable storage structure

Future Improvements

Possible future improvements include:

adding a processed layer

adding metadata tables

implementing data quality checks

automating partition management

Local Development Note

During local development, the same data lake structure is mirrored inside the project directory.

Example:

data/raw/
data/curated/

This allows the pipeline to be developed locally before using Google Cloud Storage in the full cloud workflow.