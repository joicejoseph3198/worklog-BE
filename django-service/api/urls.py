from django.urls import path
from .views import (TaskCreateView, TaskGetByIdView, TaskGetByDateView, TaskUpdateView, TaskDeleteView, TaskCopyFromDateView, NotesGetByDateView,
                    NoteUpsertDeleteView, ScheduleUpsertDeleteView, ScheduleFetchView)

urlpatterns=[
    path("task/create", TaskCreateView.as_view(), name="task-create"),
    path("task/copy", TaskCopyFromDateView.as_view(), name="copy-tasks"),
    path("task/all/day", TaskGetByDateView.as_view(), name="task-by-date"),
    path("task/update/", TaskUpdateView.as_view(), name="update-task"),
    path("task/delete/<int:id>", TaskDeleteView.as_view(), name="delete-task"),
    path("task/<str:id>", TaskGetByIdView.as_view(), name="task-by-id"),
    path("note/fetch", NotesGetByDateView.as_view(), name="note-by-date"),
    path("note/upsert", NoteUpsertDeleteView.as_view(), name="note-upsert"),
    path("schedule/upsert", ScheduleUpsertDeleteView.as_view(), name="schedule-upsert"),
    path("schedule",ScheduleFetchView.as_view(), name="schedule-by-date")
]
