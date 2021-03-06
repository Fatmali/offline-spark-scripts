from builtins import range
from datetime import timedelta

import airflow
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['fali@ampath.or.ke'],
    'email_on_failure': True,
    'email_on_retry': True,
    'start_date': datetime.now() - timedelta(minutes=20),
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    dag_id='batch_nightly_delete_job',
    default_args=default_args,
    schedule_interval='0 0 * * *',
    dagrun_timeout=timedelta(minutes=60),
)

bash_command = """
                cd /usr/local/airflow/spark-scripts/batch-rebuild-scripts &&\
                spark-submit --master local[*] --driver-class-path /usr/local/airflow/spark-jars/mysql-connector-java-8.0.16.jar \
                --jars /usr/local/airflow/spark-jars/mysql-connector-java-8.0.16.jar --driver-memory 8g \
                --executor-memory 1g \
                --packages org.apache.spark:spark-sql_2.11:2.4.0,org.apache.bahir:spark-sql-cloudant_2.11:2.3.2,com.datastax.spark:spark-cassandra-connector_2.11:2.4.0,commons-configuration:commons-configuration:1.9 \
                day_0_rebuild_couch.py
               """

run_this = BashOperator(
    task_id='batch_nightly_delete_job',
    bash_command=bash_command,
    dag=dag,
)


if __name__ == "__main__":
    dag.cli()
