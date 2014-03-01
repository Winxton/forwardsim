from tasks import add
import time
from celery.task.control import revoke


task_id = add.delay(0, 2).id

print task_id
time.sleep(5)

print "terminating task"
revoke(task_id, terminate=True)

"""
from celery.task.control import revoke

revoke('967c961a-8297-4d0b-8102-6feb3bd4bcab')
"""