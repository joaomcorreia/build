from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class AITool(models.Model):
    """
    Available AI tools and their configuration.
    """
    TOOL_TYPES = [
        ('content_generator', 'Content Generator'),
        ('image_generator', 'Image Generator'),
        ('seo_optimizer', 'SEO Optimizer'),
        ('text_improver', 'Text Improver'),
        ('translator', 'Translator'),
        ('code_generator', 'Code Generator'),
        ('design_assistant', 'Design Assistant'),
    ]
    
    name = models.CharField(max_length=100)
    tool_type = models.CharField(max_length=30, choices=TOOL_TYPES)
    description = models.TextField()
    
    # Configuration
    is_active = models.BooleanField(default=True)
    requires_api_key = models.BooleanField(default=True)
    cost_per_request = models.DecimalField(max_digits=6, decimal_places=4, default=0.0010)
    
    # Limits
    max_requests_per_hour = models.IntegerField(default=100)
    max_requests_per_day = models.IntegerField(default=1000)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.tool_type})"


class AIRequest(models.Model):
    """
    Track AI tool usage and requests.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tool = models.ForeignKey(AITool, on_delete=models.CASCADE, related_name='requests')
    
    # Request details
    prompt = models.TextField()
    parameters = models.JSONField(default=dict, blank=True)
    
    # Response
    response_data = models.JSONField(default=dict, blank=True)
    output_text = models.TextField(blank=True)
    output_files = models.JSONField(default=list, blank=True)  # URLs/paths to generated files
    
    # Status and timing
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    processing_time = models.FloatField(null=True, blank=True)  # in seconds
    
    # Cost and usage
    tokens_used = models.IntegerField(default=0)
    cost = models.DecimalField(max_digits=8, decimal_places=6, default=0.000000)
    
    # Error handling
    error_message = models.TextField(blank=True)
    retry_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.tool.name} - {self.status} - {self.created_at}"


class ContentTemplate(models.Model):
    """
    Predefined templates for content generation.
    """
    TEMPLATE_CATEGORIES = [
        ('blog', 'Blog Posts'),
        ('product', 'Product Descriptions'),
        ('service', 'Service Pages'),
        ('about', 'About Us'),
        ('landing', 'Landing Pages'),
        ('email', 'Email Marketing'),
        ('social', 'Social Media'),
        ('seo', 'SEO Content'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=TEMPLATE_CATEGORIES)
    description = models.TextField()
    
    # Template content
    prompt_template = models.TextField()
    example_output = models.TextField(blank=True)
    
    # Configuration
    is_active = models.BooleanField(default=True)
    is_premium = models.BooleanField(default=False)
    usage_count = models.IntegerField(default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.category})"


class GeneratedContent(models.Model):
    """
    Store generated content for reuse and versioning.
    """
    CONTENT_TYPES = [
        ('text', 'Text Content'),
        ('html', 'HTML Content'),
        ('css', 'CSS Styles'),
        ('javascript', 'JavaScript Code'),
        ('json', 'JSON Data'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ai_request = models.ForeignKey(AIRequest, on_delete=models.CASCADE, related_name='generated_content')
    template = models.ForeignKey(ContentTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Content details
    title = models.CharField(max_length=200)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES, default='text')
    content = models.TextField()
    
    # Usage tracking
    is_used = models.BooleanField(default=False)
    used_in_page = models.CharField(max_length=100, blank=True)  # Page ID where content is used
    used_in_component = models.CharField(max_length=100, blank=True)  # Component ID
    
    # Versioning
    version = models.IntegerField(default=1)
    parent_content = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Quality metrics
    readability_score = models.FloatField(null=True, blank=True)
    seo_score = models.FloatField(null=True, blank=True)
    word_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - v{self.version}"


class AIUsageStats(models.Model):
    """
    Track AI usage statistics for analytics and billing.
    """
    # Time period
    date = models.DateField()
    
    # Tool usage
    tool = models.ForeignKey(AITool, on_delete=models.CASCADE, related_name='usage_stats')
    
    # Statistics
    total_requests = models.IntegerField(default=0)
    successful_requests = models.IntegerField(default=0)
    failed_requests = models.IntegerField(default=0)
    
    # Performance metrics
    avg_processing_time = models.FloatField(default=0.0)
    total_tokens_used = models.IntegerField(default=0)
    total_cost = models.DecimalField(max_digits=10, decimal_places=6, default=0.000000)
    
    # Popular prompts/templates
    top_prompts = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['date', 'tool']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.tool.name} - {self.date}"


class AIConfiguration(models.Model):
    """
    Tenant-specific AI tool configuration and preferences.
    """
    # API Keys (encrypted)
    openai_api_key = models.CharField(max_length=200, blank=True)
    anthropic_api_key = models.CharField(max_length=200, blank=True)
    google_ai_api_key = models.CharField(max_length=200, blank=True)
    
    # Default settings
    default_model = models.CharField(max_length=50, default='gpt-3.5-turbo')
    default_temperature = models.FloatField(default=0.7)
    default_max_tokens = models.IntegerField(default=1000)
    
    # Usage limits
    monthly_request_limit = models.IntegerField(default=100)
    daily_request_limit = models.IntegerField(default=10)
    cost_limit_per_month = models.DecimalField(max_digits=8, decimal_places=2, default=50.00)
    
    # Feature flags
    content_generation_enabled = models.BooleanField(default=True)
    image_generation_enabled = models.BooleanField(default=False)
    code_generation_enabled = models.BooleanField(default=False)
    seo_optimization_enabled = models.BooleanField(default=True)
    
    # Quality settings
    enable_content_review = models.BooleanField(default=True)
    auto_save_generated_content = models.BooleanField(default=True)
    enable_version_control = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "AI Configuration"
