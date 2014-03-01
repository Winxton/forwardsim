from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

import json

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/start/", methods=['POST'])
def start():
    print request.path
    print request.method
    data = json.loads(request.data)
    exec data['code']
    print data
    #stuff()
    return "OK"

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
