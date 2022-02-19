from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)

    image = models.ImageField(blank=True, null=True)
    thumbnail = models.ImageField(blank=True, null=True)
