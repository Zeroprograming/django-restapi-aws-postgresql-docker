from rest_framework import viewsets
from ..serializers import  CategorySerializer

from company_manager.models import Category

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
