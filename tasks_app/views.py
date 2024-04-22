from django.http.response import HttpResponse
from tasks_app.tasks import first_task


def task1_view(request, *args, **kwargs):
    result = first_task.delay()  # Asynchronously execute the task
    print(result)
    return HttpResponse(f'Task ID: {result.id}')
