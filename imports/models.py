from django.db import models

class ImportJob(models.Model):
    status = models.CharField(max_length=20)
    file_path = models.TextField()
    processed_rows = models.IntegerField(default=0)
    total_rows = models.IntegerField(default=0)
    error_message = models.TextField(blank=True)


