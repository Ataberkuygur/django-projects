from django.urls import path
from .views import TaskCreate, TaskDelete, TaskIndex, TaskListDelete, TaskUpdate, Done_or_Not

app_name = 'Task'

urlpatterns = [
    path("", TaskIndex, name="index"),
    path("task/create/", TaskCreate, name="task_create"),
    path("task/update/<slug>/", TaskUpdate, name="update"),
    path("task/delete/<slug>/", TaskDelete, name="delete"),
    path("task/delete/all/<slug>/", TaskListDelete, name="task_delete_all"),
    path("task/done_or_not/<slug>/", Done_or_Not, name="done_or_not"),
]
