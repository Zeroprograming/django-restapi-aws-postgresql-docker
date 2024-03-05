from django.db import models

class Enterprise(models.Model):
    nit = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, unique=True)
    country = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @staticmethod
    def get_all_enterprises():
        return Enterprise.objects.all()