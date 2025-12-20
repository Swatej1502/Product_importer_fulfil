import time
import requests
from celery import shared_task
from .models import Webhook

@shared_task
def send_webhook(webhook_id, payload):
    webhook = Webhook.objects.get(id=webhook_id)

    if not webhook.enabled:
        return

    start = time.time()

    try:
        response = requests.post(
            webhook.url,
            json=payload,
            timeout=5
        )

        duration = int((time.time() - start) * 1000)

        webhook.last_test_status = response.status_code
        webhook.last_test_time_ms = duration
        webhook.last_test_error = ""

    except Exception as e:
        webhook.last_test_status = None
        webhook.last_test_time_ms = None
        webhook.last_test_error = str(e)

    webhook.save()
