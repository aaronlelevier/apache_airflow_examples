from datetime import timedelta

import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(2),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'python_tutorial',
    default_args=default_args,
    description='python_tutorial DAG',
    schedule_interval=timedelta(days=1),
)


def my_args(*args, **kwargs):
    print(args)
    print(kwargs)


t1 = PythonOperator(
    task_id='my_func_task_id',
    provide_context=True,
    python_callable=my_args,
    dag=dag)
