from django.urls import path
from .views import (
    list_webhooks,
    create_webhook,
    update_webhook,
    delete_webhook,
    test_webhook,
    webhooks_page,
)

urlpatterns = [
    path("ui/", webhooks_page),  
    path("", list_webhooks),
    path("create/", create_webhook),
    path("update/<int:webhook_id>/", update_webhook),
    path("delete/<int:webhook_id>/", delete_webhook),
    path("test/<int:webhook_id>/", test_webhook),
]
