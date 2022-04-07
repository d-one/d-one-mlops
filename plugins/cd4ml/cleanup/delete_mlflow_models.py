from pprint import pprint
from mlflow.tracking import MlflowClient


if __name__ == "__main__":
    client = MlflowClient()
    for rm in client.list_registered_models():
        pprint(dict(rm), indent=4)
        client.delete_registered_model(name=rm.name)
