from rest_framework import viewsets
from ..serializers import  CategorySerializer

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from company_manager.models import Category

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    @action(detail=False, methods=['get'], url_path='', url_name='list', permission_classes=[], authentication_classes=[])
    def list_categories(self, request):
        # Esta acción no requiere autenticación ni permisos
        return super().list(request)
    
    # Especificar la autenticación y los permisos para todas las acciones
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]