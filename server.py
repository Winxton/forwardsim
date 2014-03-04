from flask import Flask
from flask import render_template
from flask import request, session

from celery import Celery
from celery.task.control import revoke
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
app.secret_key = 'some random secret key'

from flaskcelery.tasks import rates

# webapp

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/start/", methods=['POST'])
def start():
    print request.path
    print request.method

    # temporarily store session (very hacky, should store in DB)
    print session

    data = json.loads(request.data)
<<<<<<< HEAD

    print data['code']

    response = rates.delay(data['code'])
=======
    
    #exec data['code']
    #print data['code']

    task_id = rates.delay().id
    session['TASK_ID'] = task_id

    print task_id
>>>>>>> origin/master

    return "OK"

@app.route("/stop/", methods=['POST'])
def stop():
    print "stuff123"
    print session

    response = {}
    response['status'] = 'fail'

    # a task is already running
    if "TASK_ID" not in session:
        response['status'] = 'no_task_running'
    else:
        task_id = session['TASK_ID']
        print ("A task is running with id: %s" % task_id)
        revoke(task_id, terminate=True)
        print ("TASK REVOKED")

        del(session['TASK_ID'])
        response['status'] = 'task_stopped'

    print response

    return json.dumps(response)

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
