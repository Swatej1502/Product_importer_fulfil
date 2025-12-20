from django.urls import path
from .views import (
    list_products,
    create_product,
    update_product,
    delete_product,
    delete_all_products
)

urlpatterns = [
    path("", list_products),
    path("create/", create_product),
    path("update/<int:product_id>/", update_product),
    path("delete/<int:product_id>/", delete_product),
    path("delete-all/", delete_all_products),
]
