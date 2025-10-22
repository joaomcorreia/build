from rest_framework import serializers
from .models import AITool, AIRequest, ContentTemplate, GeneratedContent, AIUsageStats

class AIToolSerializer(serializers.ModelSerializer):
    """Serializer for AITool model"""
    
    class Meta:
        model = AITool
        fields = ['id', 'name', 'description', 'tool_type', 'provider', 
                 'model_name', 'api_endpoint', 'is_active', 'cost_per_request', 
                 'max_requests_per_day', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class AIRequestSerializer(serializers.ModelSerializer):
    """Serializer for AIRequest model"""
    
    class Meta:
        model = AIRequest
        fields = ['id', 'tool', 'request_type', 'input_data', 'output_data', 
                 'status', 'error_message', 'cost', 'processing_time', 
                 'created_at', 'completed_at']
        read_only_fields = ['id', 'created_at', 'completed_at', 'processing_time']

class ContentTemplateSerializer(serializers.ModelSerializer):
    """Serializer for ContentTemplate model"""
    
    class Meta:
        model = ContentTemplate
        fields = ['id', 'name', 'description', 'template_type', 'content', 
                 'variables', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class GeneratedContentSerializer(serializers.ModelSerializer):
    """Serializer for GeneratedContent model"""
    
    class Meta:
        model = GeneratedContent
        fields = ['id', 'request', 'content_type', 'title', 'content', 
                 'metadata', 'is_approved', 'feedback', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class AIUsageStatsSerializer(serializers.ModelSerializer):
    """Serializer for AIUsageStats model"""
    
    class Meta:
        model = AIUsageStats
        fields = ['id', 'date', 'total_requests', 'successful_requests', 
                 'failed_requests', 'total_cost', 'avg_processing_time', 
                 'created_at']
        read_only_fields = ['id', 'created_at']