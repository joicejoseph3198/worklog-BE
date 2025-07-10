from django.urls import path
from .views import TaskCreateView, TaskGetByIdView, TaskGetByDate

urlpatterns=[
    path("", TaskCreateView.as_view(), name="task-create"),
    path("<str:id>/", TaskGetByIdView.as_view(), name="task-by-id"),
    path("all", TaskGetByDate.as_view(), name="task-by-date"),
]
