from aipo.celery import app
from pycaret.anomaly import load_model, predict_model
from utils.config.settings import MODEL
import pandas as pd


@app.task
def run(params):
    data = {
        'hour':[params['hour']],
        'pdis':[params['pdis']],
        'cpu':[params['cpu']],
        'mem':[params['mem']]
    }
    df = pd.DataFrame(data)
    anomaly = load_model(MODEL)
    return predict_model(anomaly, data=df).to_dict()
