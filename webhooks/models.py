from django.db import models

class Webhook(models.Model):
    EVENT_CHOICES = [
        ("import_completed", "Import Completed"),
        ("product_created", "Product Created"),
        ("product_updated", "Product Updated"),
        ("product_deleted", "Product Deleted"),
        ("bulk_deleted", "Bulk Deleted"),
    ]

    url = models.URLField()
    event_type = models.CharField(max_length=50, choices=EVENT_CHOICES)
    enabled = models.BooleanField(default=True)

    last_test_status = models.IntegerField(null=True, blank=True)
    last_test_time_ms = models.IntegerField(null=True, blank=True)
    last_test_error = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
