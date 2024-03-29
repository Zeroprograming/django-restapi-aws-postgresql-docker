from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from company_manager.models import Enterprise
from ..serializers import EnterpriseSerializer
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class EnterpriseViewSet(viewsets.ModelViewSet):
    queryset = Enterprise.objects.all()
    serializer_class = EnterpriseSerializer
    
    @action(detail=False, methods=['get'], url_path='', url_name='list', permission_classes=[], authentication_classes=[])
    def list_enterprises(self, request):
        # Esta acción no requiere autenticación ni permisos
        return super().list(request)
    
    @action(detail=False, methods=['get'], url_path='search', url_name='search', permission_classes=[permissions.AllowAny], authentication_classes=[])
    def search(self, request):
        data = request.query_params
        id = data.get('id')
        nit = data.get('nit')
        name = data.get('name')
        country = data.get('country')
        
        enterprises = Enterprise.objects.all()
        
        if name:
            enterprises = enterprises.filter(name__icontains=name)
        
        if nit:
            enterprises = enterprises.filter(nit=nit)
        
        if id:
            enterprises = enterprises.filter(id=id)
            
        if country:
            enterprises = enterprises.filter(country=country)
        
        serializer = EnterpriseSerializer(enterprises, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
        # Especificar la autenticación y los permisos para todas las acciones
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]