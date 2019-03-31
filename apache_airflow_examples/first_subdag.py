import os
import datetime
from datetime import timedelta

import airflow
from airflow.example_dags.subdags.subdag import subdag
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.subdag_operator import SubDagOperator
from airflow.operators.python_operator import PythonOperator

import utils

logger = utils.get_logger(__name__)

ONE_DAY_AGO = datetime.timedelta(days=1)

FIVE_MINUTES = datetime.timedelta(minutes=5)


def filename_if_exists(**kwargs):
    logger.info('kwargs: %s', kwargs)

    f = kwargs.get('f')

    if not os.path.isfile(f):
        ret = 'NOTHING'

    name, _ = os.path.splitext(os.path.basename(f))
    ret = name

    logger.info('ret: %s', ret)


def bool_if_file_exists(f):
    return os.path.isfile(f)


def subdag_log_filename_if_exists(parent_dag_name, child_dag_name, args, **kwargs):
    dag_subdag = DAG(
        dag_id='%s.%s' % (parent_dag_name, child_dag_name),
        default_args=args,
    )

    PythonOperator(
        task_id=child_dag_name,
        default_args=args,
        python_callable=filename_if_exists,
        dag=dag_subdag,
    )

    return dag_subdag


DAG_NAME = 'first_subdag'

FILENAME = __file__

args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(2),
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

start = DummyOperator(
    task_id='start',
    default_args=args,
    dag=dag,
)

section_1 = SubDagOperator(
    task_id='section-1',
    subdag=subdag_log_filename_if_exists(DAG_NAME, 'section-1', args),
    default_args=args,
    dag=dag,
)

end = DummyOperator(
    task_id='end',
    default_args=args,
    dag=dag,
)

start >> section_1 >> end
