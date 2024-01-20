from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from datetime import datetime


dag = DAG(
    dag_id='src_parquet_to_psql',
    start_date=datetime(2024, 1, 18, 0, 0, 0),
    schedule_interval="@once",
    catchup=False,
    tags=['parquet', 'psql'],
)


def parquet_to_psql(**context):
    execution_date = context['data_interval_start'].in_timezone('Asia/Bangkok')
    
    import pandas as pd
    import psycopg2
    from sqlalchemy import create_engine
    from sqlalchemy.exc import SQLAlchemyError
    import os
    import glob
    from io import StringIO

    engine = create_engine('postgresql+psycopg2://datawow_de_test:datawow_de_test@postgres_datawow_de_test/datawow_de_test', echo=False)
    schema_name = "datawow"
    table_name = "de_test"
    engine.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")

    parquet_directory = "/opt/airflow/data_source/data_sample"
    list_parquet_files = glob.glob(os.path.join(parquet_directory, "*.parquet"))
    
    df = pd.read_parquet(list_parquet_files[0])
    df.to_sql(name=table_name, schema=schema_name, con=engine, index=False, if_exists='replace')
    columns_name = df.columns
    
    conn = psycopg2.connect(
        dbname='datawow_de_test',
        user='datawow_de_test',
        password='datawow_de_test',
        host='postgres_datawow_de_test',
        port='5432'
    )
    cur = conn.cursor()

    batch_size = 20
    for i in range(1, len(list_parquet_files), batch_size):
        batch_files = list_parquet_files[i:i + batch_size]
        dfs = [pd.read_parquet(file) for file in batch_files]
        combined_df = pd.concat(dfs, ignore_index=True)

        sio = StringIO()
        combined_df.to_csv(sio, index=False, header=False)
        sio.seek(0)
        with conn.cursor() as c:
            c.copy_expert(
                sql=f"""
                COPY {schema_name}.{table_name} (
                    {', '.join(columns_name)}
                ) FROM STDIN WITH CSV""",
                file=sio
            )
            conn.commit()
    

    
generate_parquet = BashOperator(task_id="generate_parquet", bash_command='cd /opt/airflow/data_source && python /opt/airflow/scripts/sampledata_new.py', do_xcom_push=False, dag=dag)
parquet_to_psql_task = PythonOperator(task_id="parquet_to_psql_task", python_callable=parquet_to_psql, dag=dag)

generate_parquet >> parquet_to_psql_task