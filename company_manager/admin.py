from django.contrib import admin
from .models.category import Category
from .models.client import Client
from .models.enterprise import Enterprise
from .models.order import Order
from .models.product import Product
from .models.user import User
from django.contrib.auth.admin import UserAdmin
from .models.user import UserType


# Register your models here.
admin.site.register(Category)
admin.site.register(Client)
admin.site.register(Enterprise)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(User, UserAdmin)
admin.site.register(UserType)
