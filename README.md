# D ONE MLOps

Full Maching Learning Lifecycle using open source technologies. This repository offers a fully functioning end-to-end MLOps training pipeline that runs with Docker Compose. The goal is to (1) provide you with a MLOps training tool and (2) give you a head start when building your production machine learning (“ML”) pipeline for your own project.

The built pipeline uses:
- DVC to track data
- MLflow to track experiments and register models
- Apache Airflow to orchestrate the MLOps pipeline
- Docker


## How to work with this repo
1. Clone the repository to your machine
   ```
   git@github.com:d-one/d-one-mlops.git
   ```
 
2. Install Docker

   check https://docs.docker.com/get-docker/ and install according to your OS

3. Run
   ```
   echo -e "AIRFLOW_UID=$(id -u)" > .env
   ```

4. Run
   ```
   pip install docker-compose
   ```

5. Run
   ```
   docker-compose up 
   ```

6.  Open handout.md

## Requirements
Please find the requirements of airflow environment [here](dockerfiles/airflow/requirements.txt)


## Access
- http://localhost:8080 airflow, credentials airflow/airflow
- http://localhost:8888 jupyterlab, token cd4ml
- http://localhost:5000 mlflow
- http://localhost:9001 minio S3 server credentials mlflow_access/mlflow_secret
- http://localhost:5555 flower for monitoring celery cluster.



## Cleanup
Run the following to stop all running docker containers through docker compose
```
docker-compose stop
```
or run the following to stop and delete all running docker containers through docker
```
docker stop $(docker ps -q)
```
```
docker rm $(docker ps -aq)
```
Finally run the following to delete all (named) volumes
```
docker volume rm $(docker volume ls -q)
```
