from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from .models import MediaFile, MediaFolder, ImageOptimization, MediaLibrarySettings
from .serializers import (
    MediaFileSerializer, MediaFolderSerializer, 
    ImageOptimizationSerializer, MediaLibrarySettingsSerializer
)

class MediaFileViewSet(viewsets.ModelViewSet):
    """ViewSet for managing media files"""
    queryset = MediaFile.objects.all()
    serializer_class = MediaFileSerializer
    
    def get_queryset(self):
        # Filter by current tenant
        return MediaFile.objects.filter(tenant=self.request.tenant)

class MediaFolderViewSet(viewsets.ModelViewSet):
    """ViewSet for managing media folders"""
    queryset = MediaFolder.objects.all()
    serializer_class = MediaFolderSerializer
    
    def get_queryset(self):
        # Filter by current tenant
        return MediaFolder.objects.filter(tenant=self.request.tenant)

class ImageOptimizationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing image optimizations"""
    queryset = ImageOptimization.objects.all()
    serializer_class = ImageOptimizationSerializer
    
    def get_queryset(self):
        # Filter by current tenant's files
        return ImageOptimization.objects.filter(media_file__tenant=self.request.tenant)

class MediaUploadView(APIView):
    """View for uploading media files"""
    
    def post(self, request):
        # Handle file upload logic here
        return Response({'status': 'uploaded'}, status=status.HTTP_200_OK)

class BulkUploadView(APIView):
    """View for bulk uploading media files"""
    
    def post(self, request):
        # Handle bulk upload logic here
        return Response({'status': 'bulk uploaded'}, status=status.HTTP_200_OK)

class OptimizeImageView(APIView):
    """View for optimizing images"""
    
    def post(self, request, file_id):
        try:
            media_file = MediaFile.objects.get(id=file_id, tenant=request.tenant)
            # Handle image optimization logic here
            return Response({'status': 'optimized'}, status=status.HTTP_200_OK)
        except MediaFile.DoesNotExist:
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)

class MediaLibrarySettingsView(APIView):
    """View for managing media library settings"""
    
    def get(self, request):
        try:
            settings = MediaLibrarySettings.objects.get(tenant=request.tenant)
            return Response(MediaLibrarySettingsSerializer(settings).data)
        except MediaLibrarySettings.DoesNotExist:
            return Response({'error': 'Settings not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        # Handle settings update
        return Response({'status': 'settings updated'}, status=status.HTTP_200_OK)
