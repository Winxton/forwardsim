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
)
celery = make_celery(flask_app)

script = """
def initialize(context):
    print "HELLO"
    context.stuff = "stuff"
    context.max = 10000

def handle_data(context):
    print "DO STUFF"
    print context.stuff
    print context.max
"""


token = "b47aa58922aeae119bcc4de139f7ea1e-27de2d1074bb442b4ad2fe0d637dec22"


@celery.task()
def rates():
    alg = TradingAlgorithm(script=script)
    alg.run()