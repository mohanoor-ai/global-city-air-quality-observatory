# Global Air Quality Data Pipeline

An end-to-end data engineering pipeline that collects global air quality measurements from OpenAQ, processes the data in a cloud data warehouse, and visualizes pollution trends using an interactive dashboard.

This project demonstrates a complete modern data engineering workflow including ingestion, orchestration, transformation, and analytics.

---

# Problem Description

Air pollution is one of the largest environmental health risks globally. Millions of people are exposed to unsafe air quality levels every day.

Despite thousands of monitoring stations worldwide, air quality data is fragmented and difficult to analyze at a global scale.

This project builds an automated data pipeline that collects and analyzes global air pollution data in order to answer questions such as:

- Which countries have the highest air pollution levels?
- How do pollution levels change over time?
- Which cities have the worst air quality?
- Are pollution levels improving globally?

---

# Dataset

The dataset comes from the **OpenAQ platform**, which aggregates air quality data from official monitoring stations worldwide.

Source:

https://openaq.org

The dataset contains measurements for the following pollutants:

- PM2.5
- PM10
- NO2
- SO2
- CO
- O3

Dataset characteristics:

- 100+ countries
- 12,000+ monitoring stations
- Millions of measurements
- Updated every 10–60 minutes

---

# Architecture

The pipeline follows a modern **ELT architecture**.
