Data Ingestion

This folder contains the ingestion scripts for the Air Quality Data Pipeline.

The ingestion stage is responsible for downloading air quality measurements from the OpenAQ dataset and storing them as raw files.

These files represent the first step of the data pipeline.

Data Source

The dataset used in this project comes from OpenAQ.

OpenAQ provides global air pollution measurements collected from monitoring stations.

Example pollutants included in the dataset:

PM2.5

PM10

NO2

SO2

CO

O3

These measurements include information such as:

pollutant type

measured value

timestamp

location

coordinates

Purpose of the Ingestion Layer

The ingestion step performs the following tasks:

download air quality data from the source

convert the data into tabular format

store the dataset as Parquet files

prepare the data for the data lake

The ingestion layer does not modify the data structure significantly.

It focuses on capturing the data in its raw form.

Output

The ingestion script generates raw Parquet files.

Example local output:

data/raw/air_quality_raw.parquet

These files represent the raw layer of the pipeline.

Script

The main ingestion script is:

download_air_quality_data.py

This script:

calls the OpenAQ API

downloads measurement data

converts the results into a pandas DataFrame

saves the dataset as a Parquet file

Running the Ingestion Script

Run the ingestion script using the project environment.

Example:

uv run python ingestion/download_air_quality_data.py

After execution, the raw dataset will appear in:

data/raw/
Next Stage

After ingestion, the next stage of the pipeline will:

upload raw data to Google Cloud Storage

clean and normalize the dataset

generate curated datasets

load data into BigQuery