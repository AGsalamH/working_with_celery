import time
from celery import group, chain, shared_task


class TaskRouter:
    def route_for_task(self, task, *args, **kwargs):
        '''This router method exptects task name is in `<queue_name>:<task_name>` format.
         If NOT it routes all tasks to the default queue'''
        if ':' not in task:
            return {'queue': 'celery'}

        namespace, _ = task.split(':')
        return {'queue': namespace}


@shared_task(name='my_queue:first_task', rate_limit='1/m') # one task per minute
def first_task():
    time.sleep(3)
    return 'First task completed!'

@shared_task(name='my_queue:second_task')
def second_task():
    time.sleep(3)
    return 'Second task completed!'


tasks_group = group([first_task.s(), second_task.s()])

# ----------- CHAINING ----------------------

@shared_task(name='my_queue:t1')
def t1():
    return 'Task 1'

@shared_task(name='my_queue:t2')
def t2(result):
    return 'Task 2'



task_chain = chain(t1.s(), t2.s())
