"""
Code that goes along with the Airflow tutorial located at:
https://github.com/apache/airflow/blob/master/airflow/example_dags/tutorial.py
"""
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta


from datetime import datetime, timedelta

default_args = {
    'owner': 'Airflow',
    'depends_on_past': False,
    'start_date': datetime(2019,1,1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}


dag = DAG('test1', default_args=default_args, schedule_interval=timedelta(minutes=1))


def print_hello(**kwargs):
    print('hello, airflow!')


op = PythonOperator(
    task_id='print_the_context',
    provide_context=True,
    python_callable=print_hello,
    dag=dag,
)

op2 = PythonOperator(
    task_id='print_the_context2',
    provide_context=True,
    python_callable=print_hello,
    dag=dag,
)


op >> op2
