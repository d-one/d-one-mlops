from asyncio.log import logger
import subprocess
import os
import argparse

import logging

logger = logging.getLogger(__name__)


def launch_api_endpoint(model=None):
    """Launches the REST API endpoint through a docker container. 

    Args:
        model (_type_, optional): A model name in mlflow. If model is set the latest model with production tag is taken. Defaults to None.

    Raises:
        ValueError: If run_id and model ar both empty.
    """

    if model is not None:
        model_env = "-e MLFLOW_MODEL={}".format(model)
    else:
        raise ValueError("model must be set")

    bashCommand = "docker run -p 5000:5000 \
        "+model_env+"\
        -e MLFLOW_TRACKING_USERNAME={} \
        -e MLFLOW_TRACKING_PASSWORD={} \
        -e AZURE_STORAGE_ACCESS_KEY={} \
        -e AZURE_STORAGE_CONNECTION_STRING={} \
        -e MLFLOW_TRACKING_URI={} \
        -d \
        deployed_model".format(
        # username for tracking server
        os.environ.get("MLFLOW_TRACKING_USERNAME"),
        # password for tracking server
        os.environ.get("MLFLOW_TRACKING_PASSWORD"),
        # access key for azure storage
        os.environ.get("AZURE_STORAGE_ACCESS_KEY"),
        # connection string for azure storage
        os.environ.get("AZURE_STORAGE_CONNECTION_STRING"),
        os.environ.get("MLFLOW_TRACKING_URI"),              # tracking uri
    )

    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description='Launches REST Endpoint')
    argparser.add_argument('run_id', type=str, help='run_id to deploy')
    args = argparser.parse_args()
    launch_api_endpoint(args.run_id)
