from django.urls import path
from .views import list_products, bulk_delete

urlpatterns = [
    path("", list_products),
    path("delete-all/", bulk_delete),
]
