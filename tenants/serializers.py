from rest_framework import serializers
from .models import Client, Domain

class ClientSerializer(serializers.ModelSerializer):
    """Serializer for Client (tenant) model"""
    
    class Meta:
        model = Client
        fields = ['schema_name', 'name', 'description', 'business_name', 
                 'business_type', 'contact_email', 'is_active', 
                 'subscription_plan', 'subscription_expires', 'ai_tools_enabled',
                 'custom_domain_enabled', 'advanced_analytics_enabled',
                 'max_pages', 'max_storage_mb', 'max_monthly_ai_requests',
                 'primary_color', 'secondary_color', 'logo_url',
                 'created_on', 'auto_create_schema', 'auto_drop_schema']
        read_only_fields = ['created_on', 'auto_create_schema', 'auto_drop_schema']

class DomainSerializer(serializers.ModelSerializer):
    """Serializer for Domain model"""
    
    class Meta:
        model = Domain
        fields = ['domain', 'tenant', 'is_primary']
        read_only_fields = []