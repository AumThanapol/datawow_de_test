# DataWow DE Test

## Table of Contents

- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Running Data Pipeline](#running-data-pipeline)
- [Troubleshooting](#troubleshooting)
- [Contact](#contact)


## Installation

### Prerequisites:

- Git
- Docker
- Docker compose

### Steps:

- Clone the repository: `git clone <repository-url>`.
- Download additional files (if not already present):
    - [requirements.txt](requirements.txt)
    - [sampledata_new.py](sampledata_new.py)


## Running the Project

1. Open a terminal window in the cloned repository's directory.
2. Run the command `docker-compose up -d` to start the Docker containers.
3. Wait for approximately 30 seconds for the containers to initialize.
4. Open the Airflow web interface in a web browser at http://localhost:8080.

If you encounter issues, please refer to [Troubleshooting](#troubleshooting).


## Running Data Pipeline

1. Open the Airflow web interface in a web browser at http://localhost:8080.
2. Log in with username `airflow_datawow_de` and password `airflow_datawow_de`.
3. Select the **src_parquet_to_psql** DAG in the Airflow UI.
4. Start the data pipeline by clicking the **Unpause toggle**.

### src_parquet_to_psql

1. **Initialize the DAG**: 
   - Scheduled to run once (`@once`).
    - Handles Parquet data generation and PostgreSQL transfer.

2. **Generate Parquet Data**:
    - Utilizes `generate_parquet`, a BashOperator task.
    - Executes `sampledata_new.py` to generate Parquet files.

3. **Parquet to PostgreSQL Transfer**:
    - Activates `parquet_to_psql_task`, following `generate_parquet`.
    - Uses PythonOperator to execute `parquet_to_psql`.
    - Transfers data from Parquet to PostgreSQL, with error handling.
   
If you encounter issues, please refer to [Troubleshooting](#troubleshooting).


## Troubleshooting

### [Running the Project](#running-the-project)
Web Interface Issues:
- Ensure Docker containers are active (`docker-compose ps`).
- Restart any stopped containers (`docker-compose up -d`).
- Check terminal and Docker logs for errors.

### [Running Data Pipeline](#running-data-pipeline)
DAG Status Issues:
- Examine the DAG's logs for anomalies.
- Directly access Airflow logs within Docker for detailed insights.


## Contact

For any questions or assistance, please contact aumthanapol1998@gmail.com

Thank you.