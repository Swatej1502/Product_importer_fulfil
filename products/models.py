from django.db import models
from django.db.models.functions import Lower

# Create your models here.
class Product(models.Model):
    sku = models.CharField(max_length=64)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(Lower('sku'), name='sku_lower_idx'),
        ]
        constraints = [
            models.UniqueConstraint(
                Lower('sku'),
                name='unique_sku_lower'
            )
        ]
