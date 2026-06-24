FROM apache/airflow:3.0.0-python3.12

USER airflow

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt \
    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-3.0.0/constraints-3.12.txt"
