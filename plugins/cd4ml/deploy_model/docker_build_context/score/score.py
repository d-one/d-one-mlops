import numpy as np
import mlflow
import pandas as pd

import os

if os.environ.get("MLFLOW_RUN_ID") is not None:
    logged_model = "runs:/{}/model".format(os.environ.get("MLFLOW_RUN_ID"))
elif os.environ.get("MLFLOW_MODEL") is not None:
    logged_model="models:/{}/Production".format(os.environ.get("MLFLOW_MODEL"))

def init():
    global model
    model = mlflow.pyfunc.load_model(logged_model)
    
def run(data):
    input_data = pd.read_json(data.get("data"))
    result = model.predict(input_data)
    return {"result": result.tolist(), "model_run_id": model.metadata.run_id}