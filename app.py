# pip freeze > requirements.txt
from flask import Flask
from flask import jsonify
import requests


app = Flask(__name__)


URL = "https://lab.karpov.courses/hardml-api/module-5/get_secret_number"
# return_secret_number
@app.route('/')
def hello_world():  # put application's code here

    secret_number = None

    while secret_number is None:
        r = requests.get(url=URL)
        if r.headers.get('content-type') == 'application/json':
            data = r.json()
            secret_number = data['secret_number']
    return jsonify(secret_number=secret_number)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
