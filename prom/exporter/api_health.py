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

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

PING = os.environ.get("PING")
ANOMALY_API = os.environ.get("ANOMALY_API")

RESPONSE_TIME_GAUGE = prom.Gauge('sample_external_url_response_ms', 'Url response time in ms', ["url"])
ANOMALY_ML = prom.Gauge('ml_monitoring_infra', 'Anomaly Detection with ML', ["url"])


def get_response(url: str) -> dict:
    response = requests.get(url)
    response_time = response.elapsed.total_seconds()
    return response_time


def post_infra():
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

async def anomaly_detection():
    while True:
        response_time = get_response(PING)
        RESPONSE_TIME_GAUGE.labels(url=PING).set(response_time)
        async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
            async with session.post(ANOMALY_API, json=post_infra()) as resp:
                result = await resp.json()
                ANOMALY_ML.labels(url=ANOMALY_API).set(100 if result['task_payload'][0]['result']['Anomaly']['0'] == 1 else 0)
                time.sleep(5)



if __name__ == '__main__':
    prom.start_http_server(8009)
    asyncio.run(anomaly_detection())
