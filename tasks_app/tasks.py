import time
from celery import group, shared_task


class TaskRouter:
    def route_for_task(self, task, *args, **kwargs):
        '''This router method exptects task name is in `<queue_name>:<task_name>` format.
         If NOT it routes all tasks to the default queue'''
        if ':' not in task:
            return {'queue': 'celery'}

        namespace, _ = task.split(':')
        return {'queue': namespace}


@shared_task(name='my_queue:first_task')
def first_task():
    time.sleep(3)
    return 'First task completed!'

@shared_task(name='my_queue:second_task')
def second_task():
    time.sleep(3)
    return 'Second task completed!'


tasks_group = group([first_task.s(), second_task.s()])
