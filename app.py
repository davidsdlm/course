# pip freeze > requirements.txt
from flask import Flask
from flask import jsonify
from first import init_redis, init_replica
import requests
import socket


app = Flask(__name__)


secret_number = None
URL = "https://lab.karpov.courses/hardml-api/module-5/get_secret_number"
# return_secret_number
@app.route('/')
def hello_world():  # put application's code here
    return jsonify(secret_number=secret_number)


if __name__:
    while secret_number is None:
        r = requests.get(url=URL)
        if r.headers.get('content-type') == 'application/json':
            data = r.json()
            secret_number = data['secret_number']

    app.run(debug=True, use_reloader=True)

    redis_password = 'lolkek123'
    redis_host = '65.109.236.1'
    redis_port = 6379
    # 8001 - insight
    init_redis(redis_host, redis_port, redis_password)

    hostname = socket.gethostname()
    host = socket.gethostbyname(hostname)
    port = "5000"
    name = "replica_name"
    init_replica(host, port, name)
#     debug=True, use_reloader=True
