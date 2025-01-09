# views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ServiceCategory, ServiceSubcategory, Service
from .serializers import ServiceSerializer
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated , IsAdminUser, AllowAny
from .serializers import ServiceCategorySerializer, ServiceSubcategorySerializer, ServiceSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Brochure, News
from .serializers import BrochureSerializer, NewsSerializer

class BrochureViewSet(viewsets.ModelViewSet):
    queryset = Brochure.objects.all()
    serializer_class = BrochureSerializer

    def update(self, request, *args, **kwargs):
        # Debug: ver qué datos llegan
        print("Request data:", request.data)
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        serializer = self.get_serializer(
            instance, 
            data=request.data, 
            partial=True  # Permitir actualización parcial
        )
        
        if not serializer.is_valid():
            print("Errores de validación:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            self.perform_update(serializer)
            return Response(serializer.data)
        except Exception as e:
            print("Error al actualizar:", str(e))
            return Response(
                {"detail": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all().order_by('-publication_date')
    serializer_class = NewsSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Log para debugging
        print("Datos recibidos:", request.data)
        print("Datos validados:", serializer.validated_data)
        
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()
    
    def get_object(self):
        """
        Permite buscar tanto por id como por slug
        """
        queryset = self.get_queryset()
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup = self.kwargs[lookup_url_kwarg]
        
        # Intenta buscar por ID primero
        try:
            obj = queryset.get(id=lookup)
        except (ValueError, News.DoesNotExist):
            # Si no es un ID válido o no se encuentra, busca por slug
            obj = queryset.get(slug=lookup)
            
        self.check_object_permissions(self.request, obj)
        return obj

class ServiceCategoryViewSet(viewsets.ModelViewSet):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # Para rutas protegidas

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]  # Público para GET
        return [IsAuthenticated()]

class ServiceSubcategoryViewSet(viewsets.ModelViewSet):
    queryset = ServiceSubcategory.objects.all()
    serializer_class = ServiceSubcategorySerializer

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class RegisterAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]  # Solo admins pueden crear otros admins
    
    def post(self, request):
        try:
            # Validar datos requeridos
            if not request.data.get('username') or not request.data.get('password'):
                return Response({
                    'error': 'Username y password son requeridos'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Validar que el username no exista
            if User.objects.filter(username=request.data['username']).exists():
                return Response({
                    'error': 'Este username ya está en uso'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Validar contraseña
            try:
                validate_password(request.data['password'])
            except ValidationError as e:
                return Response({
                    'error': e.messages
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Crear el usuario admin
            user = User.objects.create_user(
                username=request.data['username'],
                email=request.data.get('email', ''),
                password=request.data['password'],
                is_staff=True,  # Hace al usuario un admin
                is_superuser=request.data.get('is_superuser', False)  # Opcional
            )
            
            return Response({
                'message': 'Usuario administrador creado exitosamente',
                'username': user.username
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminCheckView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        print("Admin check requested for user:", request.user.username)  # Debug
        print("Is staff:", request.user.is_staff)  # Debug
        print("Is superuser:", request.user.is_superuser)  # Debug
        
        return Response({
            'is_admin': True,
            'username': request.user.username,
            'status': 'success'
        })