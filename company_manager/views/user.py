from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from company_manager.models import User,UserType
from ..serializers import UserSerializer, UserTypeSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=False, methods=['post'], url_path='login', url_name='login', permission_classes=[permissions.AllowAny])
    def login(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        
        # Verificar si el usuario existe
        if not User.objects.filter(email=email).exists():
            return Response({'error': 'User does not exist!'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.get(email=email)
        
        # Verificar si la contraseña es correcta
        if not check_password(password, user.password):
            return Response({'error': 'Invalid password!'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Si el usuario existe y la contraseña es correcta, generar un token de autenticación
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], url_path='sing-up', url_name='sing-up', permission_classes=[permissions.AllowAny])
    def sing_up(self, request):
        data = request.data
        email = data.get('email')
    
        # Verificar si ya existe un usuario con el mismo correo electrónico
        if User.objects.filter(email=email).exists():
            return Response({'error': 'User with this email already exists!'}, status=status.HTTP_400_BAD_REQUEST)
    
        # Si no existe, continuar con la creación del usuario
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
    
            token = Token.objects.create(user=user)
            return Response({'status': 'User created successfully!', 'token': token.key}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserTypeViewSet(viewsets.ModelViewSet):
    queryset = UserType.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserTypeSerializer

