# MLOps

Full Maching Learning Lifecycle using open source technologies


## How to work with this repo
1. Clone the repository to your machine
   ```
   git@github.com:d-one/cd4ml-workshop.git
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
Run the following to stop all running docker containers
```
docker stop $(docker ps -q)
```
Run the following to delete all (stoped) docker containers
```
docker rm $(docker ps -aq)
```
Run the following to delete all (named) volumes
```
docker volume rm $(docker volume ls -q)
```
