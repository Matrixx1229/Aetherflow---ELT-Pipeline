# Aetherflow---ELT-Pipeline

# 🌌 AetherFlow: End-to-End ELT Pipeline

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![Airflow](https://img.shields.io/badge/Airflow-2.9-00C7D4?logo=apache-airflow&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-Core-FF694B?logo=dbt&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?logo=postgresql&logoColor=white)

**A containerized data engineering project that automates the extraction, loading, and transformation of data using a modern stack.**

---

## 📖 About The Project

AetherFlow is a robust ELT (Extract, Load, Transform) pipeline designed to simulate a real-world data infrastructure. It moves raw operational data from a source database to a data warehouse and transforms it into analytical models ready for business intelligence.

### 🏗️ Architecture


graph LR
        A[Source Postgres] -->|Extract & Load (Python)| B[Destination Postgres]
        B -->|Transform (dbt)| C[Analytical Models]
        D[Apache Airflow] -->|Orchestrates| A
        D -->|Orchestrates| C


The workflow follows these steps:

Extract & Load: A custom Python script extracts raw tables (films, actors, etc.) from the Source Database and loads them into the Destination Database.

Transform: dbt (Data Build Tool) takes the raw data, cleans it (Staging models), and joins it to create a final film_ratings analytical table.

Orchestration: Apache Airflow manages the entire workflow, ensuring dependencies are met and tasks run on schedule.

### 🛠️ Tech Stack
Orchestration: Apache Airflow (running inside Docker)

Transformation: dbt Core (with dbt-postgres adapter)

Containerization: Docker & Docker Compose

Database: PostgreSQL (v17)

Language: Python 3.11

📂 Project Structure
```
AetherFlow/
├── airflow/               # Airflow configuration
│   ├── Dockerfile         # Custom Airflow image with dbt & postgres-client
│   └── requirements.txt   # Python dependencies
├── dags/                  # Airflow DAGs (elt_dags.py)
├── custom_project/        # dbt project folder
│   ├── models/            # SQL models (stg_films, film_ratings, etc.)
│   ├── profiles.yml       # dbt connection configuration
│   └── dbt_project.yml    # dbt project settings
├── elt/                   # ELT scripts
│   └── elt_script.py      # Python script for data extraction & loading
├── source_db_init/        # Initialization SQL for source DB
├── docker-compose.yaml    # Main infrastructure configuration

└── README.md              # Project Documentation
```
### 🚀 Getting Started
Follow these instructions to run the pipeline locally.

Prerequisites
- Docker Desktop installed and running.

Installation:
1. Clone the repository: git clone [https://github.com/your-username/AetherFlow.git](https://github.com/your-username/AetherFlow.git)
cd AetherFlow/elt
2. Build and Run the Containers: This command spins up the Source DB, Destination DB, Airflow Webserver, Scheduler, and initializes the databases. - (docker-compose up --build)
3. Access the Airflow UI: Open your browser and navigate to:

URL: http://localhost:8080

Username: airflow

Password: ****

### 🏃‍♂️ Usage
In the Airflow UI, find the DAG named elt_and_dbt.

Unpause the DAG by clicking the toggle switch (turn it Blue).

Click the Play Button (▶️) under Actions to trigger a run manually.

Click on the DAG name and go to the Graph View to watch the pipeline execute in real-time.

### 📊 Transformations (dbt)

The dbt project creates the following lineage:

Staging Models (stg_): Raw tables are materialized as views to protect the source data.

Final Model (film_ratings):

Joins films, actors, and film_actors.

Calculates a rating_category (Good, Poor, Excellent) based on user ratings.

Aggregates the list of actors for each film into a single string.

### 🔮 Future Improvements

Visualization: Connect a BI tool like Metabase or Streamlit to visualize the film_ratings table.

Data Quality: Add more complex dbt test cases (e.g., accepted values for ratings).

CI/CD: Automate the testing of dbt models using GitHub Actions.

