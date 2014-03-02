from flask import Flask
from flask import render_template
from flask import request
from celery import Celery
import json

"""
from flaskcelery.tasks import make_celery

app = Flask('server')

app.config.update(
    CELERY_BROKER_URL='amqp://guest@localhost//',
)
celery = make_celery(app)

# celery task

@celery.task()
def add_together(a, b):
    import time
    time.sleep(5)
    return a + b
"""

app = Flask(__name__)

from flaskcelery.tasks import add_together

# webapp

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/start/", methods=['POST'])
def start():
    print request.path
    print request.method
    data = json.loads(request.data)
    exec data['code']
    print data['code']
    
    result = add_together.delay(23, 42)

    return "OK"

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
