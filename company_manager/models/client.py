from django.db import models
from .user import User
from .order import Order

class Client(models.Model):
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)
    
    orders = models.ManyToManyField(Order, related_name='clients')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)