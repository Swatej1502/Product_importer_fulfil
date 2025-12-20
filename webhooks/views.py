from django.shortcuts import render

# Create your views here.
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Webhook
from .tasks import send_webhook

def webhooks_page(request):
    return render(request, "webhooks.html")

def list_webhooks(request):
    return JsonResponse(list(Webhook.objects.values()), safe=False)

@csrf_exempt
def create_webhook(request):
    data = json.loads(request.body)
    w = Webhook.objects.create(
        url=data["url"],
        event_type=data["event_type"],
        enabled=data.get("enabled", True)
    )
    return JsonResponse({"id": w.id})

@csrf_exempt
def update_webhook(request, webhook_id):
    data = json.loads(request.body)
    w = Webhook.objects.get(id=webhook_id)
    w.url = data["url"]
    w.event_type = data["event_type"]
    w.enabled = data.get("enabled", True)
    w.save()
    return JsonResponse({"ok": True})

@csrf_exempt
def delete_webhook(request, webhook_id):
    Webhook.objects.filter(id=webhook_id).delete()
    return JsonResponse({"ok": True})

@csrf_exempt
def test_webhook(request, webhook_id):
    payload = {
        "event": "test",
        "message": "This is a test webhook"
    }
    send_webhook.delay(webhook_id, payload)
    return JsonResponse({"ok": True})
