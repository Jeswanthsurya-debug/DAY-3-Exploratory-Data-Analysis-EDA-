# DAY-3-Exploratory-Data-Analysis-EDA-
# Mutual Fund Analytics & Ingestion Pipeline

An end-to-end data engineering and Exploratory Data Analysis (EDA) pipeline designed to process, ingest, and analyze multi-layered mutual fund transaction data, portfolio disclosures, and historical market benchmark performances.

---

## 📁 Repository Structure

*   **`data/`**: Subdirectory containing raw layer source files (including master data, historical NAVs, investor transactions, portfolio disclosures, and benchmark data).
*   **`EDA_Analysis.ipynb`**: Interactive Jupyter Notebook mapping out visual trends, demographic behavior breakdowns, asset concentrations, and timeline tracking.
*   **`build_database.py`**: Initializes the schema structures and compiles individual data streams.
*   **`data_ingestion.py`**: Cleans, parses, maps data types, and populates the local relational database.
*   **`run_queries.py`**: Validates data integrity and runs complex analytical queries directly against the database engine.
*   **`bluestock_mf.db`**: SQLite database generated locally by the automated engine pipeline.

---

## 📊 Analytical Pipeline Architecture

The workflow comprehensively spans 10 distinct analytical layers, mapping data from raw CSV files into an optimized relational environment:

1. **Exploratory Data Analysis**: Visualizes market trajectory behaviors, investor age/gender brackets, and asset distribution patterns using `matplotlib` and `seaborn`.
2. **Database Schema Compilation**: Models table logic and structures inside a local SQLite storage instance.
3. **Automated ETL Ingestion**: Implements programmatic type-casting and structural mapping for transactional streams.
4. **Business Intelligence Querying**: Extracts granular descriptive statistics, state-by-state volumes, and product breakdown reports (SIP vs. Lumpsum vs. Redemption).

---

## 🚀 Execution & Setup Guide

### 1. Environment Configuration
Ensure your environment satisfies the required packages specified in `requirements.txt`:
```bash
pip3 install -r requirements.txt
2. Run Database Engine Setup
Initialize the database instance to establish target table relations:
python3 build_database.py

3. Run Data Ingestion Pipeline
Parse and populate raw data sources into the relational database engine:
python3 data_ingestion.py

4. Execute Validation & Reporting Metrics
Run optimized analytical reporting queries directly from the database:
python3 run_queries.py
