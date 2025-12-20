from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json
from .models import Product

def list_products(request):
    qs = Product.objects.all().order_by("id")

    # ---- FILTERS ----
    sku = request.GET.get("sku")
    name = request.GET.get("name")
    description = request.GET.get("description")
    active = request.GET.get("active")

    if sku:
        qs = qs.filter(sku__icontains=sku)
    if name:
        qs = qs.filter(name__icontains=name)
    if description:
        qs = qs.filter(description__icontains=description)
    if active in ["true", "false"]:
        qs = qs.filter(active=(active == "true"))

    # ---- PAGINATION ----
    page = int(request.GET.get("page", 1))
    paginator = Paginator(qs, 10)  # 10 products per page
    page_obj = paginator.get_page(page)

    return JsonResponse({
        "products": list(page_obj.object_list.values()),
        "page": page,
        "total_pages": paginator.num_pages
    })

@csrf_exempt
def create_product(request):
    data = json.loads(request.body)
    p = Product.objects.create(
        sku=data["sku"],
        name=data["name"],
        description=data.get("description", ""),
        active=data.get("active", True)
    )
    return JsonResponse({"id": p.id})

@csrf_exempt
def update_product(request, product_id):
    data = json.loads(request.body)
    p = Product.objects.get(id=product_id)
    p.sku = data["sku"]
    p.name = data["name"]
    p.description = data.get("description", "")
    p.active = data.get("active", True)
    p.save()
    return JsonResponse({"ok": True})

@csrf_exempt
def delete_product(request, product_id):
    Product.objects.filter(id=product_id).delete()
    return JsonResponse({"ok": True})

@csrf_exempt
def delete_all_products(request):
    Product.objects.all().delete()
    return JsonResponse({"ok": True})
