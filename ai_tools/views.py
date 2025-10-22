from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from .models import AITool, AIRequest, ContentTemplate, GeneratedContent, AIUsageStats
from .serializers import (
    AIToolSerializer, AIRequestSerializer, ContentTemplateSerializer,
    GeneratedContentSerializer, AIUsageStatsSerializer
)

class AIToolViewSet(viewsets.ModelViewSet):
    """ViewSet for managing AI tools"""
    queryset = AITool.objects.all()
    serializer_class = AIToolSerializer
    
    def get_queryset(self):
        # Filter by current tenant
        return AITool.objects.filter(tenant=self.request.tenant)

class AIRequestViewSet(viewsets.ModelViewSet):
    """ViewSet for managing AI requests"""
    queryset = AIRequest.objects.all()
    serializer_class = AIRequestSerializer
    
    def get_queryset(self):
        # Filter by current tenant
        return AIRequest.objects.filter(tenant=self.request.tenant)

class ContentTemplateViewSet(viewsets.ModelViewSet):
    """ViewSet for managing content templates"""
    queryset = ContentTemplate.objects.all()
    serializer_class = ContentTemplateSerializer
    
    def get_queryset(self):
        # Filter by current tenant
        return ContentTemplate.objects.filter(tenant=self.request.tenant)

class GeneratedContentViewSet(viewsets.ModelViewSet):
    """ViewSet for managing generated content"""
    queryset = GeneratedContent.objects.all()
    serializer_class = GeneratedContentSerializer
    
    def get_queryset(self):
        # Filter by current tenant
        return GeneratedContent.objects.filter(tenant=self.request.tenant)

class GenerateContentView(APIView):
    """View for generating content with AI"""
    
    def post(self, request):
        # Handle content generation logic here
        return Response({'status': 'content generated'}, status=status.HTTP_200_OK)

class GenerateImageView(APIView):
    """View for generating images with AI"""
    
    def post(self, request):
        # Handle image generation logic here
        return Response({'status': 'image generated'}, status=status.HTTP_200_OK)

class OptimizeSEOView(APIView):
    """View for optimizing SEO with AI"""
    
    def post(self, request):
        # Handle SEO optimization logic here
        return Response({'status': 'SEO optimized'}, status=status.HTTP_200_OK)

class ImproveTextView(APIView):
    """View for improving text with AI"""
    
    def post(self, request):
        # Handle text improvement logic here
        return Response({'status': 'text improved'}, status=status.HTTP_200_OK)

class AIUsageStatsView(APIView):
    """View for AI usage statistics"""
    
    def get(self, request):
        try:
            stats = AIUsageStats.objects.filter(tenant=request.tenant)
            return Response(AIUsageStatsSerializer(stats, many=True).data)
        except AIUsageStats.DoesNotExist:
            return Response({'error': 'Stats not found'}, status=status.HTTP_404_NOT_FOUND)
