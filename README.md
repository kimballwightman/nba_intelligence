# NBA Intelligence

An analytics engineering portfolio project built on BigQuery, dbt, and Airflow. Ingests NBA basketball data, models it through staging and mart layers, and orchestrates the pipeline end-to-end.

## Stack

- **Warehouse**: Google BigQuery
- **Transformations**: dbt Core 2.0 (Fusion engine) with `dbt-bigquery`
- **Orchestration**: Apache Airflow 3 (Docker)
- **Source data**: Basketball Reference, NBA Stats API

## Repo Structure

```
nba_intelligence/
├── dbt/                  # dbt project — models, seeds, macros, tests
├── airflow/              # Airflow DAGs, Dockerfile, docker-compose
├── data/                 # Exploratory notebooks and sample data
└── scripts/              # Utility scripts
```

## Getting Started

### dbt

1. Copy `dbt/profiles.yml.sample` to `~/.dbt/profiles.yml` and fill in your GCP project and service account keyfile path.
2. Install dbt: `pip install dbt-core dbt-bigquery`
3. Verify connection:
   ```bash
   cd dbt/
   dbt debug
   ```

### Airflow

1. Copy `airflow/.env.template` to `airflow/.env` and set `AIRFLOW_UID` (`echo "AIRFLOW_UID=$(id -u)"`).
2. Start the stack:
   ```bash
   cd airflow/
   docker compose up airflow-init   # first time only
   docker compose up -d
   ```
3. Open the Airflow UI at [http://localhost:8080](http://localhost:8080) (default: `airflow` / `airflow`).
