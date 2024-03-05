from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name