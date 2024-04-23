# working_with_celery

--- 

TODO:
- TASK PRIORITIZATION
- TASK GROUPING
- TASK CHAINING
- MONITORING


### Initialization

```python
# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

```

---

### Configurations

```python
CELERY_BROKER_URL = environ.get('CELERY_BROKER', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = environ.get('CELERY_BACKEND', 'redis://redis:6379/0')
# To use Django ORM as a CELERY_BACKEND
# We need to pip `install install django-celery-results`
# then put django_celery_results in our installed_apps 
# Finally set RESULT_BACKEND :down
CELERY_RESULT_BACKEND = 'django-db' # use django orm as result backend
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True # Avoid warning in celery logs
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
```

---

### NOTES

- Make sure to put this piece of code inside project.__init__.py
    
    ```python
    # This will make sure the app is always imported when
    # Django starts so that shared_task will use this app.
    from .celery_app import app as celery_app
    
    __all__ = ("celery_app",)
    
    ```
    

---

After that we’re ready to create tasks and execute them inside our celery worker

---

### TASK ROUTES

- To implement TASK routing, Specify a `Queue` from which each celery worker listens to.
    
    ```python
    celery -A core.celery_app worker --loglevel=info -Q queue1
    celery -A core.celery_app worker --loglevel=info -Q queue2
    ```
    
- And inside `settings.py`
    - Configure `CELERY_TASK_ROUTES` option
        
        ```python
        CELERY_TASK_ROUTES = {
            'myapp.tasks.task1': {
                'queue': 'queue1'
            },
            
            'myapp.tasks.task2': {
                'queue': 'queue2'
            },
          
        	  # We can use wildcards `*` or even REGEX
        	  # This selects all tasks inside the specified path.
            'myapp.tasks.*': {
        	      'queue': 'queue2'
            },
            
        }
        
        ```
        
    
    <aside>
    💡  default queue (named “celery” for historical reasons).
    
    </aside>
    

---

### TASK DYNAMIC ROUTES

- Instead of configuring the `task_routes` per task, we can tell Celery to use a custom class instead by specifying the path to that class.
`CELERY_TASK_ROUTES = ‘myapp.task_router.TaskRouter’`

---

Celery expects the method `route_for_task` that passes the task name as its first argument

```python
class TaskRouter:
    def route_for_task(self, task, *args, **kwargs):
        if ':' not in task:
            return {'queue': 'default'}

        namespace, _ = task.split(':')
        return {'queue': namespace}

```

<aside>
💡 Make sure to specify name of task eg: @shared_task(name=’queue:task_name’)

</aside>

---

### TASK PRIORITIZATION

<aside>
💡 CELERY does NOT natively support task prioritizing when using Redis as a message broker,  We may consider using another broker such as : RabbitMQ

</aside>
