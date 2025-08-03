from django.urls import path

from .views import TaskDetailView
from .views import TaskListCreateView

urlpatterns = [
    # Task URLs
    path("<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("", TaskListCreateView.as_view(), name="task-list-create"),
]
