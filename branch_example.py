"""
Example of PythonOperator and BranchPythonOperator

Helpful resources:

- https://www.astronomer.io/guides/airflow-branch-operator/
- https://airflow.apache.org/howto/operator.html#pythonoperator
- https://airflow.apache.org/tutorial.html
- http://michal.karzynski.pl/blog/2017/03/19/developing-workflows-with-apache-airflow/

NEXT: connect the dots DAG and SubDag by making creating a simple example one

- models.DAG
- subdag_operator.SubDagOperator
"""
import logging
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator


def get_logger(module):
    """
    Returns a configured standard library `logger`

    Args:
        module (__name__) of the client code calling this function
    """
    logger = logging.getLogger(module)
    logger.setLevel(logging.INFO)

    # create a logging format
    formatter = logging.Formatter(
        '%(asctime)s - %(filename)s:%(lineno)d - %(funcName)s - %(levelname)s - %(message)s')

    handler = logging.StreamHandler()
    handler.setLevel(logging.ERROR)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


logger = get_logger(__name__)


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2015, 6, 1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG('branch_example', default_args=default_args, schedule_interval=timedelta(days=1))

start = DummyOperator(task_id='start', dag=dag)

def print_all(*args, **kwargs):
    logger.info('print all')
    logger.info('args: %s', args)
    logger.info('kwargs: %s', kwargs)

def check_callable(*args, **kwargs):
    return 'foo'

check = BranchPythonOperator(task_id='check', python_callable=check_callable, dag=dag)

foo = PythonOperator(task_id='foo', python_callable=print_all, provide_context=True, dag=dag)

bar = PythonOperator(task_id='bar', python_callable=print_all, provide_context=True, dag=dag)

start >> check
check >> foo
check >> bar
