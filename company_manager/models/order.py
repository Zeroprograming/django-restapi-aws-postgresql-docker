from django.db import models
from .product import Product

class Order(models.Model):
    
    products = models.ManyToManyField(Product, related_name='orders')
    
    payment_currency = models.CharField(max_length=3, default='USD')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @staticmethod
    def get_all_orders():
        return Order.objects.all()

    def __str__(self):
        return self.total