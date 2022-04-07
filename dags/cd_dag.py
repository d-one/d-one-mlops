# Author:      CD4ML Working Group @ D ONE
# Description: Script that defines and creates the CI Airflow DAG (the MLOps 
#              training pipeline). If the Airflow scheduler and webserver are
#              running, you can visit the UI on localhost:8080 and trigger & 
#              monitor the pipeline
# ================================================================================

from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from airflow.utils.timezone import datetime
from cd4ml.deploy_model import launch_api_endpoint

_model = "my_model"

default_args = {
    'owner': 'cd4ml',
    'depends_on_past': False,
    'start_date': days_ago(0),
    'retries': 1,
    'retry_delay': timedelta(seconds=5),
}

dag = DAG(
    'cd_pipeline',
    default_args=default_args,
    description='Continuous Deployment Pipeline',
    schedule_interval=timedelta(days=1),
)

with dag:

    kill_running_docker_container = BashOperator(
        task_id='kill_running_docker_container',
        bash_command="docker kill $(docker ps --filter ancestor=deployed_model -q)",
    )

    build_docker_image = BashOperator(
        task_id='build_docker_image',
        bash_command='docker build $PROJECT_PATH/cd4ml/deploy_model/docker_build_context -t deployed_model',
        trigger_rule="all_done",
    )

    launch_api = PythonOperator(
        task_id='launch_api_endpoint',
        python_callable=launch_api_endpoint,
        op_kwargs={
            'model': _model
        }
    )

    kill_running_docker_container >> build_docker_image >> launch_api
