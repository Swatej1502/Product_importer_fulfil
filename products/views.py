from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .models import Product

def list_products(request):
    data = list(Product.objects.values())
    return JsonResponse(data, safe=False)

def bulk_delete(request):
    Product.objects.all().delete()
    return JsonResponse({"ok": True})
