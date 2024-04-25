from django.http.response import HttpResponse
from tasks_app.tasks import first_task, tasks_group, task_chain


def task1_view(request, *args, **kwargs):
    result = first_task.delay()  # Asynchronously execute the task
    print(result)
    return HttpResponse(f'Task ID: {result.id}')


def group_view(request, *args, **kwargs):
    result = tasks_group.apply_async() # Asynchronously execute the task
    print(result)
    return HttpResponse(f'Group ID: {result.id}')

def chain_view(request, *args, **kwargs):
    result = task_chain.apply_async() # Asynchronously execute the task
    print(result)
    return HttpResponse(f'Chain ID: {result.id}')
