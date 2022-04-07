# Author:      CD4ML Working Group @ D ONE
# Description: Script that defines and creates the CI Airflow DAG (the MLOps 
#              training pipeline). If the Airflow scheduler and webserver are
#              running, you can visit the UI on localhost:8080 and trigger & 
#              monitor the pipeline
# ================================================================================

import os
from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago
from airflow.utils.timezone import datetime
from cd4ml.data_processing import ingest_data
from cd4ml.data_processing import split_train_test
from cd4ml.data_processing import validate_data
from cd4ml.data_processing import transform_data
from cd4ml.model_training import train_model
from cd4ml.model_validation import validate_model
from cd4ml.model_validation import push_model
from cd4ml.data_processing.track_data import track_data

### SET A UNIQUE MODEL NAME (e.g. "model_<YOUR NAME>"):
_model_name = "my_model"
### SET A UNIQUE EXPERIMENT NAME (e.g. "experiment_<YOUR NAME>"):
_mlflow_experiment_name = "my_experiment"

_raw_data_dir = '/data/batch1'
# _raw_data_dir = '/data/batch2'


_root_dir = "/"
_data_dir = "/data"
_data_files = {
    'raw_data_file': os.path.join(_data_dir, 'data.csv'),
    'raw_train_file': os.path.join(_data_dir, 'data_train.csv'),
    'raw_test_file': os.path.join(_data_dir, 'data_test.csv'),
    'transformed_x_train_file': os.path.join(_data_dir, 'x_train.csv'),
    'transformed_y_train_file': os.path.join(_data_dir, 'y_train.csv'),
    'transformed_x_test_file': os.path.join(_data_dir, 'x_test.csv'),
    'transformed_y_test_file': os.path.join(_data_dir, 'y_test.csv'),
}


if not _root_dir:
    raise ValueError('PROJECT_PATH environment variable not set')


default_args = {
    'owner': 'cd4ml',
    'depends_on_past': False,
    'start_date': days_ago(0),
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}

dag = DAG(
    'ci_pipeline',
    default_args=default_args,
    description='Continuous Integration Pipeline',
    schedule_interval=timedelta(days=1),
)

with dag:
    pass
    data_ingestion = PythonOperator(
        task_id='data_ingestion',
        python_callable=ingest_data,
        op_kwargs={'input_folder': _raw_data_dir,
                   'data_files': _data_files}
    )
    
    data_split = PythonOperator(
        task_id='data_split',
        python_callable=split_train_test,
        op_kwargs={'data_files': _data_files,
                   'n_days_test': 20}
    )

    data_validation = PythonOperator(
        task_id='data_validation',
        python_callable=validate_data,
        op_kwargs={'data_files': _data_files,
                   'configs_dir': _data_dir}
    )

    data_transformation = PythonOperator(
        task_id='data_transformation',
        python_callable=transform_data,
        op_kwargs={'data_files': _data_files}
    )

    model_training = PythonOperator(
        task_id='model_training',
        python_callable=train_model,
        op_kwargs={
            'data_files': _data_files,
            'experiment_name': _mlflow_experiment_name
        }
    )

    model_validation = BranchPythonOperator(
        task_id='model_validation',
        python_callable=validate_model,
        op_kwargs={
            'data_files': _data_files,
            'model': _model_name
        },
    )

    stop = DummyOperator(
        task_id='keep_old_model',
        dag=dag,
        trigger_rule="all_done",
    )

    push_to_production = PythonOperator(
        task_id='push_new_model',
        python_callable=push_model,
        op_kwargs={
            'model': _model_name
        },
    )

    data_ingestion >> data_split >> data_validation >> data_transformation >> model_training >> model_validation >> [
        push_to_production, stop]
    data_split >> data_validation >> data_transformation >> model_validation >> [
        push_to_production, stop]
