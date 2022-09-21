import prometheus_client as prom
import requests
import time
import os
from os.path import join, dirname
from dotenv import load_dotenv
import psutil
import datetime
import aiohttp
import asyncio
import ujson
import json
import random

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

PING = os.environ.get("PING")
ANOMALY_API = os.environ.get("ANOMALY_API")

RESPONSE_TIME_GAUGE = prom.Gauge('url_response_ms', 'Url response time in ms', ["url"])
ANOMALY_ML = prom.Gauge('infra_anomaly_detection', 'Anomaly Detection with ML', ["url"])
ANOMALY_ML_RANDOM = prom.Gauge('infra_anomaly_detection_random', 'Anomaly Detection with ML Random', ["url"])


def get_response(url: str) -> dict:
    response = requests.get(url)
    response_time = response.elapsed.total_seconds()
    return response_time


def post_infra_real():
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    pdis = len(psutil.pids())
    hour_time = datetime.datetime.now().hour

    data = {
        'hour': hour_time,
        'pdis': pdis,
        'cpu': cpu,
        'mem':mem
    }
    return data

def post_infra_false():
    data = {
        'hour': random.randint(0, 23),
        'pdis': random.randint(300, 600),
        'cpu': random.randint(0, 100),
        'mem':random.randint(0, 100)
    }
    return data

async def anomaly_detection_real():
    async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
        async with session.post(ANOMALY_API, json=post_infra_real()) as resp:
            result = await resp.json()
            ANOMALY_ML.labels(url=ANOMALY_API).set(100 if result['task_payload'][0]['result']['Anomaly']['0'] == 1 else 0)

async def anomaly_detection_false():
    async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
        async with session.post(ANOMALY_API, json=post_infra_false()) as resp:
            result = await resp.json()
            ANOMALY_ML_RANDOM.labels(url=ANOMALY_API).set(100 if result['task_payload'][0]['result']['Anomaly']['0'] == 1 else 0)

def api_response():
    response_time = get_response(PING)
    RESPONSE_TIME_GAUGE.labels(url=PING).set(response_time)


if __name__ == '__main__':
    prom.start_http_server(8009)
    print ("http://localhost:8009")

    while True:
        asyncio.run(anomaly_detection_real())
        asyncio.run(anomaly_detection_false())
        api_response()
        time.sleep(5)
