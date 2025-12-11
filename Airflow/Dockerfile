FROM apache/airflow:2.9.1

USER root

# Install git, libpq-dev, postgresql-client
RUN apt-get update && \
    apt-get install -y git libpq-dev postgresql-client && \
    apt-get clean

USER airflow

# 1. Install Airflow dependencies (pandas, psycopg2)
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# 2. Install dbt in a separate Virtual Environment
# This avoids "Dependency Hell" between Airflow and dbt
RUN python -m venv /opt/airflow/dbt_venv && \
    /opt/airflow/dbt_venv/bin/pip install --no-cache-dir dbt-postgres==1.8.2

# 3. Add the dbt virtual environment to the PATH
# This allows you to run 'dbt' commands directly in BashOperator
ENV PATH="/opt/airflow/dbt_venv/bin:$PATH"