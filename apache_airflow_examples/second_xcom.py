import os
import datetime
from datetime import timedelta

import airflow
from airflow.example_dags.subdags.subdag import subdag
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.subdag_operator import SubDagOperator
from airflow.operators.python_operator import PythonOperator


DAG_NAME = 'second_xcom'

ONE_DAY_AGO = datetime.timedelta(days=1)

FIVE_MINUTES = datetime.timedelta(minutes=5)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': FIVE_MINUTES,
}

dag = DAG(
    DAG_NAME,
    description='Simple tutorial DAG',
    schedule_interval='0 12 * * *',
    start_date=datetime.datetime(2017, 3, 20),
    catchup=False
)

# xcom_pull to retrieve a value from a PythonOperator.python_callable

start = DummyOperator(
    task_id='start',
    default_args=default_args,
    dag=dag,
)

def magic_number():
    return 42

send_magic_number = PythonOperator(
    task_id='send_magic_number',
    default_args=default_args,
    python_callable=magic_number,
    dag=dag,
)

def print_magic_number(**context):
    value = context['task_instance'].xcom_pull(task_ids='send_magic_number')
    print 'magic number is: ', value


retrieve_magic_number = PythonOperator(
    task_id='retrieve_magic_number',
    default_args=default_args,
    python_callable=print_magic_number,
    provide_context=True,
    dag=dag,
)

def push_data_func(**context):
    print(context)
    context['task_instance'].xcom_push(
        key='execution_id',
        value='foobar'
    )

push_data = PythonOperator(
    task_id='push_data',
    default_args=default_args,
    python_callable=push_data_func,
    provide_context=True,
    dag=dag
)

def pull_data_func(**context):
    value = context['task_instance'].xcom_pull(
        key='execution_id',
        task_ids='push_data'
    )
    print 'manual xcom_pull value: ', value

pull_data = PythonOperator(
    task_id='pull_data',
    default_args=default_args,
    python_callable=pull_data_func,
    provide_context=True,
    dag=dag
)

end = DummyOperator(
    task_id='end',
    default_args=default_args,
    dag=dag,
)


start >> send_magic_number >> retrieve_magic_number >> push_data >> pull_data >> end
