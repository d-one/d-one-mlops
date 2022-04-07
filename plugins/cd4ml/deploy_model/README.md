### Build Docker Container

This minimal example loads a linear model from the mlflow server and builds
a rest api around it. All relevant secrets are passed as env variables to the docker run
command. An example to request the API can then be found [here](request.py)

1. Build the docker container: This uses the folder [scoring](scoring). You might have to 
    modify the [score.py](docker_build_context/score/score.py) script and the [requirements.txt](docker_build_context/score/requirements.txt)
    ```
    docker build $PROJECT_PATH/cd4ml/deploy_model/docker_build_context -t deployed_model
    ```
2. To run the docker container execute the following. You might have to adjust the ```MLFLOW_RUN_ID```
    ```
    docker run -p 5000:5000 \
        -e MLFLOW_RUN_ID=1413783b774c45b9a971fb944936a99f \
        -e MLFLOW_TRACKING_USERNAME=$MLFLOW_TRACKING_USERNAME \
        -e MLFLOW_TRACKING_PASSWORD=$MLFLOW_TRACKING_PASSWORD \
        -e AZURE_STORAGE_ACCESS_KEY=$AZURE_STORAGE_ACCESS_KEY \
        -e AZURE_STORAGE_CONNECTION_STRING=$AZURE_STORAGE_CONNECTION_STRING \
        -e MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI \
        deployed_model
    ```

