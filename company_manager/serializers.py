from rest_framework import serializers
from .models.category import Category
from .models.client import Client
from .models.enterprise import Enterprise
from .models.order import Order
from .models.product import Product
from .models.user import User
from .models.user import UserType


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'active', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
        
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'address', 'phone_number', 'country', 'user', 'orders', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
        
class EnterpriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enterprise
        fields = ('id', 'nit', 'name', 'address', 'phone_number', 'country', 'products', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'products', 'total', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'product_code', 'product_properties', 'active', 'categories', 'currencies', 'enterprise', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'type', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
        extra_kwargs = {'password': {'write_only': True}}

class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = ('id', 'name', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
    