from celery import Celery
from alglib.oandapy import oandapy
import time
from alglib.algorithm import TradingAlgorithm

from celery.backends.base import BaseBackend

def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)

    #backend = BaseBackend(app)
    #print dir(backend)

    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

from flask import Flask

flask_app = Flask(__name__)
flask_app.config.update(
    CELERY_BROKER_URL='amqp://guest@localhost//',
    CELERY_RESULT_BACKEND = 'amqp',
    CELERY_IGNORE_RESULT = False
)

celery = make_celery(flask_app)
#celery = Celery("tasks", broker='amqp://guest@localhost//', backend="amqp", ignore_result=False)

def yielder():
    for i in range(2**10):
        time.sleep(2)
        data = {}
        data['plot1'] = i
        yield data

@celery.task()

def rates():
    for progress in yielder():
        # set current progress on the task
        rates.backend.mark_as_started(
            rates.request.id,
            progress=progress)
        print progress

"""
=======
def rates(script):
    alg = TradingAlgorithm(script=script)
    alg.run()
"""
