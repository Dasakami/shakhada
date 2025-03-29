from django.urls import path
from .views import notification_list, mark_as_read

app_name = "notifications"

urlpatterns = [
    path("notifications_list", notification_list, name="notifications_list"),
    path("read/<int:notification_id>/", mark_as_read, name="mark_as_read"),
]
