from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from .models import Client, Domain
from .serializers import ClientSerializer, DomainSerializer

class ClientViewSet(viewsets.ModelViewSet):
    """ViewSet for managing tenants/clients"""
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class DomainViewSet(viewsets.ModelViewSet):
    """ViewSet for managing tenant domains"""
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    
    def get_queryset(self):
        # Filter domains by tenant
        return Domain.objects.all()

class CreateTenantView(APIView):
    """View for creating new tenants"""
    
    def post(self, request):
        # Handle tenant creation logic here
        return Response({'status': 'tenant created'}, status=status.HTTP_201_CREATED)

class SwitchTenantView(APIView):
    """View for switching between tenants"""
    
    def post(self, request, tenant_id):
        # Handle tenant switching logic here
        return Response({'status': f'switched to tenant {tenant_id}'}, status=status.HTTP_200_OK)
