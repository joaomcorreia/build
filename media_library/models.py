from django.db import models
from django.contrib.auth import get_user_model
from PIL import Image
import uuid
import os

User = get_user_model()


def get_upload_path(instance, filename):
    """Generate upload path for media files."""
    # Get file extension
    ext = filename.split('.')[-1]
    # Generate unique filename
    filename = f"{uuid.uuid4()}.{ext}"
    # Return path organized by type and date
    return f"media/{instance.file_type}/{instance.created_at.year}/{instance.created_at.month}/{filename}"


class MediaFolder(models.Model):
    """
    Folders for organizing media files within each tenant.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        if self.parent:
            return f"{self.parent.name} / {self.name}"
        return self.name
    
    def get_full_path(self):
        """Get the full path of the folder."""
        if self.parent:
            return f"{self.parent.get_full_path()} / {self.name}"
        return self.name


class MediaFile(models.Model):
    """
    Media files (images, documents, etc.) for each tenant.
    """
    FILE_TYPES = [
        ('image', 'Image'),
        ('document', 'Document'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('other', 'Other'),
    ]
    
    IMAGE_CATEGORIES = [
        ('logo', 'Logo'),
        ('header', 'Header Image'),
        ('gallery', 'Gallery Image'),
        ('product', 'Product Image'),
        ('background', 'Background Image'),
        ('icon', 'Icon'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # File information
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to=get_upload_path)
    file_type = models.CharField(max_length=20, choices=FILE_TYPES)
    original_filename = models.CharField(max_length=255)
    
    # File metadata
    file_size = models.BigIntegerField()  # in bytes
    mime_type = models.CharField(max_length=100)
    
    # Image-specific fields
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    image_category = models.CharField(max_length=20, choices=IMAGE_CATEGORIES, blank=True)
    
    # Organization
    folder = models.ForeignKey(MediaFolder, on_delete=models.SET_NULL, null=True, blank=True, related_name='files')
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")
    
    # SEO
    alt_text = models.CharField(max_length=255, blank=True)
    caption = models.TextField(blank=True)
    
    # Usage tracking
    download_count = models.IntegerField(default=0)
    last_accessed = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.original_filename
        
        # Set file metadata
        if self.file:
            self.file_size = self.file.size
            
            # Determine file type based on mime type
            if self.mime_type.startswith('image/'):
                self.file_type = 'image'
                
                # Get image dimensions for images
                try:
                    with Image.open(self.file) as img:
                        self.width, self.height = img.size
                except Exception:
                    pass
                    
            elif self.mime_type.startswith('video/'):
                self.file_type = 'video'
            elif self.mime_type.startswith('audio/'):
                self.file_type = 'audio'
            elif self.mime_type in ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
                self.file_type = 'document'
            else:
                self.file_type = 'other'
        
        super().save(*args, **kwargs)
    
    @property
    def file_size_human(self):
        """Return human-readable file size."""
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    @property
    def is_image(self):
        return self.file_type == 'image'
    
    @property
    def is_video(self):
        return self.file_type == 'video'


class ImageOptimization(models.Model):
    """
    Track image optimizations and variations.
    """
    OPTIMIZATION_TYPES = [
        ('thumbnail', 'Thumbnail (150x150)'),
        ('small', 'Small (300x300)'),
        ('medium', 'Medium (600x600)'),
        ('large', 'Large (1200x1200)'),
        ('webp', 'WebP Conversion'),
        ('compressed', 'Compressed Original'),
    ]
    
    original_file = models.ForeignKey(MediaFile, on_delete=models.CASCADE, related_name='optimizations')
    optimization_type = models.CharField(max_length=20, choices=OPTIMIZATION_TYPES)
    
    # Optimized file
    optimized_file = models.FileField(upload_to='optimized/')
    file_size = models.BigIntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    quality = models.IntegerField(default=85)
    
    # Processing info
    processing_time = models.FloatField(null=True, blank=True)  # in seconds
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['original_file', 'optimization_type']
    
    def __str__(self):
        return f"{self.original_file.name} - {self.optimization_type}"


class MediaUsage(models.Model):
    """
    Track where media files are being used.
    """
    media_file = models.ForeignKey(MediaFile, on_delete=models.CASCADE, related_name='usage')
    
    # Usage location
    content_type = models.CharField(max_length=50)  # 'page', 'component', 'website'
    object_id = models.CharField(max_length=100)
    field_name = models.CharField(max_length=100, blank=True)  # Which field uses this media
    
    # Usage context
    usage_context = models.TextField(blank=True)  # Additional context about usage
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['media_file', 'content_type', 'object_id', 'field_name']
    
    def __str__(self):
        return f"{self.media_file.name} used in {self.content_type}#{self.object_id}"


class MediaLibrarySettings(models.Model):
    """
    Tenant-specific settings for the media library.
    """
    # Storage limits
    max_file_size_mb = models.IntegerField(default=10)
    max_total_storage_gb = models.FloatField(default=1.0)
    
    # Allowed file types
    allowed_image_types = models.JSONField(default=list, blank=True)
    allowed_document_types = models.JSONField(default=list, blank=True)
    allowed_video_types = models.JSONField(default=list, blank=True)
    
    # Auto-optimization settings
    auto_optimize_images = models.BooleanField(default=True)
    auto_generate_thumbnails = models.BooleanField(default=True)
    auto_convert_to_webp = models.BooleanField(default=True)
    image_quality = models.IntegerField(default=85)
    
    # Organization settings
    auto_categorize_images = models.BooleanField(default=True)
    require_alt_text = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "Media Library Settings"
