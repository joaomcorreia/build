from rest_framework import serializers
from .models import MediaFile, MediaFolder, ImageOptimization, MediaLibrarySettings

class MediaFileSerializer(serializers.ModelSerializer):
    """Serializer for MediaFile model"""
    
    class Meta:
        model = MediaFile
        fields = ['id', 'name', 'original_name', 'file', 'file_type', 
                 'file_size', 'mime_type', 'folder', 'alt_text', 
                 'description', 'tags', 'is_public', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at', 'file_size', 'mime_type']

class MediaFolderSerializer(serializers.ModelSerializer):
    """Serializer for MediaFolder model"""
    
    class Meta:
        model = MediaFolder
        fields = ['id', 'name', 'description', 'parent', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class ImageOptimizationSerializer(serializers.ModelSerializer):
    """Serializer for ImageOptimization model"""
    
    class Meta:
        model = ImageOptimization
        fields = ['id', 'media_file', 'optimization_type', 'original_size', 
                 'optimized_size', 'compression_ratio', 'optimized_at']
        read_only_fields = ['id', 'optimized_at', 'compression_ratio']

class MediaLibrarySettingsSerializer(serializers.ModelSerializer):
    """Serializer for MediaLibrarySettings model"""
    
    class Meta:
        model = MediaLibrarySettings
        fields = ['id', 'max_file_size', 'allowed_file_types', 
                 'auto_optimize_images', 'optimization_quality', 
                 'storage_provider', 'storage_settings', 
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']