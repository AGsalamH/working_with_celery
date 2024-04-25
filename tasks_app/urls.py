from django.urls import path
from tasks_app import views as task_views


urlpatterns = [
    path('1/', task_views.task1_view),
    path('group/', task_views.group_view),
    path('chain/', task_views.chain_view),

]
