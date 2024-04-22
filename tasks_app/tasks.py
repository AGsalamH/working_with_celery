import time
from celery import shared_task


@shared_task
def first_task():
    time.sleep(3)
    return 'First task completed!'
