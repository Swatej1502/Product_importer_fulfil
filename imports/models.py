from django.db import models

# Create your models here.
class ImportJob(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PARSING', 'Parsing'),
        ('IMPORTING', 'Importing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]

    file_path = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    processed_rows = models.IntegerField(default=0)
    total_rows = models.IntegerField(default=0)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
