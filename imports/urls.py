from django.urls import path
from .views import upload, status

urlpatterns = [
    path("upload/", upload),
    path("status/<int:job_id>/", status),
]
