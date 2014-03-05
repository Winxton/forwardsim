from celery import Celery
from alglib.oandapy import oandapy
import time
from alglib.algorithm import TradingAlgorithm

def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
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

@celery.task()
def rates(script):
    alg = TradingAlgorithm(script=script)
    for plotdata in alg.run():
        rates.backend.mark_as_started(
                    rates.request.id,
                    plot_data=plotdata
                    )
        
        print plotdata