from django.db import models
from .category import Category
from .enterprise import Enterprise 

class Product(models.Model):
    name = models.CharField(max_length=100)
    product_code = models.CharField(max_length=100)
    product_properties = models.JSONField()
    active = models.BooleanField(default=True)
    
    enterprise = models.ForeignKey(Enterprise, related_name='products', on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, related_name='products')
    currencies = models.JSONField(default=list)  # Campo para almacenar las monedas
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

