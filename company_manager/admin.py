from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Category, Client, Enterprise, Order, Product, User, UserType

admin.site.register(Category)
admin.site.register(Client)
admin.site.register(Enterprise)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(UserType)

class CustomUserAdmin(BaseUserAdmin):
    ordering = ['email']  # Ordenar por el campo email en lugar de username

admin.site.register(User, CustomUserAdmin)
