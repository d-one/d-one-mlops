FROM apache/airflow:2.2.4
USER root
RUN apt-get update 
USER airflow
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt