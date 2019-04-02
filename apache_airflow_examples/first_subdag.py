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

# dir to check for files in
BASE_DIR = os.path.join(os.path.expanduser('~'), 'data/coco/annotations')

FILENAME_2 = 'captions_train2020.json'

def filename_if_exists(filename):
    f = os.path.join(BASE_DIR, filename)

    print 'f:', f

    if f and not os.path.isfile(f):
        ret = 'NOTHING'
    else:
        name, _ = os.path.splitext(os.path.basename(f))
        ret = name

    print 'ret:', ret


def bool_if_file_exists(f):
    return os.path.isfile(f)


def subdag_log_filename_if_exists(parent_dag_name, child_dag_name, default_args, filename):
    dag_subdag = DAG(
        dag_id='%s.%s' % (parent_dag_name, child_dag_name),
        default_args=default_args,
    )

    PythonOperator(
        task_id=child_dag_name,
        default_args=default_args,
        python_callable=filename_if_exists,
        op_args=[filename],
        dag=dag_subdag,
    )

    return dag_subdag


DAG_NAME = 'first_subdag'

FILENAME = __file__

default_args = {
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
    default_args=default_args,
    dag=dag,
)

section_1 = SubDagOperator(
    task_id='section-1',
    subdag=subdag_log_filename_if_exists(
        DAG_NAME, 'section-1', default_args, 'captions_train2014.json'),
    default_args=default_args,
    dag=dag,
)

end = DummyOperator(
    task_id='end',
    default_args=default_args,
    dag=dag,
)

start >> section_1 >> end
