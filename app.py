# pipreqs C:\Users\user\PycharmProjects\flaskProject
# $env:PORT=5001
# $env:REPLICA_NAME="name"
from flask import Flask, request
from flask import jsonify
from first import init_redis, close_redis, init_replica, shutdown_scheduler, init_scheduler
import requests
import sys
import signal
import os
import time
import threading
import asyncio


app = Flask(__name__)
active_requests = 0


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


@app.route('/return_secret_number')
@requests_counter
def hello_world():
    return jsonify(secret_number=secret_number)


@app.route("/")
def hello():
    time.sleep(10)
    return "none"


if __name__ == "__main__":
    # while secret_number is None:
    #     r = requests.get(url=URL)
    #     if r.headers.get('content-type') == 'application/json':
    #         data = r.json()
    #         secret_number = data['secret_number']

    # 8001 - insight
    REDIS_HOST = os.environ['REDIS_HOST']
    REDIS_PORT = os.environ['REDIS_PORT']
    REDIS_PORT = int(REDIS_PORT)
    REDIS_PASSWORD = os.environ['REDIS_PASSWORD']

    SERVICE_DISCOVER_INTERVAL = os.environ['SERVICE_DISCOVER_INTERVAL']
    SERVICE_DISCOVER_INTERVAL = int(SERVICE_DISCOVER_INTERVAL)

    HOST = os.environ['HOST']
    PORT = os.environ['PORT']
    PORT = int(PORT)
    REPLICA_NAME = os.environ['REPLICA_NAME']

    expire_time = SERVICE_DISCOVER_INTERVAL + 1
    scheduler_interval = SERVICE_DISCOVER_INTERVAL / 2

    init_redis(REDIS_HOST, REDIS_PORT, REDIS_PASSWORD)
    init_replica(HOST, PORT, REPLICA_NAME, expire_time)
    init_scheduler(scheduler_interval, HOST, PORT, REPLICA_NAME, expire_time)

    app.run(host='0.0.0.0', port=5000)

#     debug=True, use_reloader=True
