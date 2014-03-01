from celery import Celery
from celery.task.control import revoke
import time

from oandapi import oandapy

app = Celery('tasks', broker='amqp://guest@localhost//')

@app.task
def add(x, y):
    while True:
        time.sleep(1)
        r = x+y
        print ("OK " + str(r) )

@app.task
def run_trades(access_token, rate_seconds):
    while True:
    	
        time.sleep(rate_seconds)

