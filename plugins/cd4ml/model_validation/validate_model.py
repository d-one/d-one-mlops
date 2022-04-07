# Author:      CD4ML Working Group @ D ONE
# Description: Use this script to validate the model performance on an unseen
#              test set. If the new model exceeds a certain threshold and 
#              outperforms the model in production, it will be pushed to 
#              production
# ================================================================================

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)
import os
from mlflow.tracking.client import MlflowClient
import mlflow
import pandas as pd
import logging

logger = logging.getLogger(__name__)


_eta = 0.01
_min_f1_score = 0.4


def _get_performance(y, y_pred, model_name, average='macro'):
    """calculate performance metrics"""
    accuracy = accuracy_score(y, y_pred)
    precision = precision_score(y, y_pred, average='macro')
    recall = recall_score(y, y_pred, average='macro')
    f1 = f1_score(y, y_pred, average='macro')

    logger.info(f"***** performance {model_name} *****")
    logger.info(f'accuracy: {round(accuracy, 3)}')
    logger.info(f'precision: {round(precision, 3)}')
    logger.info(f'recall: {round(recall, 3)}')
    logger.info(f'f1-score: {round(f1, 3)}\n')

    return accuracy, precision, recall, f1


def _check_keys(dict_, required_keys):
    """checks if a dict contains all expected keys"""
    for key in required_keys:
        if key not in dict_:
            raise ValueError(f'input argument "data_files" is missing required key "{key}"')
        
        
def validate_model(data_files, model="LR", **kwargs):
    """
    Validate the model by comparing with the performance of the current production model.
    If performance (F1-score) of the new model exceeds a minimum threshold and the 
    performance of the current production model, the new model will be pushed to production.

    Args:
        data_files (dict): contains the following keys:
          'transformed_x_test_file': location of test input data
          'transformed_y_test_file': location of test labels
        model (str): name of the production model in mlflow
    """
    required_keys = [
        'transformed_x_test_file',
        'transformed_y_test_file',
    ]
    _check_keys(data_files, required_keys)
    
    task_instance = kwargs.get('task_instance')

    if task_instance is None:
        ValueError(
            "task_instance is required, ensure you are calling this function from an airflow task and after a training run.")

    _, latest_model_uri = task_instance.xcom_pull(task_ids='model_training')

    logger.info(f"Loading trained model {latest_model_uri}")
    latest_model = mlflow.pyfunc.load_model(latest_model_uri)

    logger.info("Loading test data")
    x_test = pd.read_csv(data_files['transformed_x_test_file'])
    y_test = pd.read_csv(data_files['transformed_y_test_file'])

    y_test_pred = latest_model.predict(x_test)
    _, _, _, f1_new = _get_performance(y_test, y_test_pred, "new model")
    
    try:
        prod_model = mlflow.pyfunc.load_model(
            model_uri=f"models:/{model}/Production"
        )
        logger.info(f"Loaded production model {model}")
    except:
        prod_model = None
        f1_old = 0
        logger.info("There is no production model yet")

    if prod_model:
        y_test_pred_old = prod_model.predict(x_test)
        _, _, _, f1_old = _get_performance(y_test, y_test_pred_old, "old model")

    assert max(f1_old, f1_new) >= _min_f1_score, \
        f"F1-score of best model {max(f1_old, f1_new)} below minimum of {_min_f1_score}"

    if f1_new > f1_old * (1 + _eta):
        logger.info("New model is best so far, pushing to production")
        return 'push_new_model'
    else:
        logger.info("New model is not better, keeping old model")
        return 'keep_old_model'