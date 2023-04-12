# pipreqs C:\Users\user\PycharmProjects\flaskProject
from flask import Flask, request
from flask import jsonify
from first import init_redis, close_redis, init_replica, shutdown_scheduler, init_scheduler
import sys
import signal
import os
import time
import threading
import requests
import json


app = Flask(__name__)
active_requests = 0


SECRET_NUMBER = os.environ.get('SECRET_NUMBER', None)
# 8001 - insight
REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = os.environ['REDIS_PORT']
REDIS_PORT = int(REDIS_PORT)
REDIS_PASSWORD = os.environ['REDIS_PASSWORD']

SERVICE_DISCOVER_INTERVAL = os.environ['SERVICE_DISCOVER_INTERVAL']
SERVICE_DISCOVER_INTERVAL = int(SERVICE_DISCOVER_INTERVAL)


def requests_counter(func):
    def _wrapper(*args, **kwargs):
        global active_requests
        active_requests += 1
        result = func(*args, **kwargs)
        active_requests -= 1
        return result
    return _wrapper


def end_all_connections(pid):
    while active_requests != 0:
        time.sleep(0.2)
    os.kill(pid, signal.SIGKILL)


def handler(sig, frame):
    if sig == signal.SIGINT or sig == signal.SIGTERM:
        shutdown_scheduler()
        close_redis()
        threading.Timer(SERVICE_DISCOVER_INTERVAL+3, end_all_connections, [os.getpid()]).start()
    else:
        sys.exit(0)


signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGTERM, handler)


secret_number = None
URL = "https://lab.karpov.courses/hardml-api/module-5/get_secret_number"


@app.route('/get_string_iris_pred')
@requests_counter
def hello_world():
    try:
        par_1 = float(request.args.get('sepal_length'))
        par_2 = float(request.args.get('sepal_width'))
        pred = par_1 * par_2
        if pred == 0:
            pred = par_1 + par_2
        if pred == 0:
            pred == 1

        threshold_0_1 = json.loads(SECRET_NUMBER)['threshold_0_1']
        threshold_1_2 = json.loads(SECRET_NUMBER)['threshold_1_2']
        class_str = None
        if pred < threshold_0_1:
            class_str = "setosa"
        elif threshold_0_1 < pred < threshold_1_2:
            class_str = "versicolor"
        elif threshold_1_2 < pred:
            class_str = "virginica"

        return jsonify({"class": pred, "class_str": class_str, "threshold_0_1": threshold_0_1, "threshold_1_2":threshold_1_2})
    except:
        return "501"


@app.route('/get_source_iris_pred')
def rmodel_first():
    try:
        par_1 = float(request.args.get('sepal_length'))
        par_2 = float(request.args.get('sepal_width'))
        pred = par_1 * par_2
        if pred == 0:
            pred = par_1 + par_2
        if pred == 0:
            pred == 1
        return jsonify({"prediction": pred})
    except:
        return "error"


HOST = os.environ['HOST']
PORT = os.environ['PORT']
PORT = int(PORT)
REPLICA_NAME = os.environ['REPLICA_NAME']

expire_time = SERVICE_DISCOVER_INTERVAL + 1
scheduler_interval = SERVICE_DISCOVER_INTERVAL / 2

init_redis(REDIS_HOST, REDIS_PORT, REDIS_PASSWORD)
init_replica(HOST, PORT, REPLICA_NAME, expire_time)
init_scheduler(scheduler_interval, HOST, PORT, REPLICA_NAME, expire_time)

# app.run(host='0.0.0.0', port=5000)

    # debug=True, use_reloader=True
