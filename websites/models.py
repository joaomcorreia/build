from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
import uuid

User = get_user_model()


class Website(models.Model):
    """
    Main website configuration for each tenant.
    Each tenant can have multiple websites.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Domain and URL configuration
    subdomain = models.CharField(max_length=50, unique=True)
    custom_domain = models.CharField(max_length=100, blank=True)
    is_published = models.BooleanField(default=False)
    
    # Design and branding
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    favicon = models.ImageField(upload_to='favicons/', blank=True, null=True)
    primary_color = models.CharField(max_length=7, default='#007bff')
    secondary_color = models.CharField(max_length=7, default='#6c757d')
    font_family = models.CharField(max_length=100, default='Arial, sans-serif')
    
    # SEO settings
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    
    # Analytics
    google_analytics_id = models.CharField(max_length=20, blank=True)
    facebook_pixel_id = models.CharField(max_length=20, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.subdomain:
            self.subdomain = slugify(self.name)
        super().save(*args, **kwargs)


class Page(models.Model):
    """
    Individual pages within a website.
    """
    PAGE_TYPES = [
        ('home', 'Home Page'),
        ('about', 'About Page'),
        ('contact', 'Contact Page'),
        ('blog', 'Blog Page'),
        ('service', 'Service Page'),
        ('product', 'Product Page'),
        ('custom', 'Custom Page'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='pages')
    
    # Page information
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    page_type = models.CharField(max_length=20, choices=PAGE_TYPES, default='custom')
    
    # Content
    content = models.TextField(blank=True)  # HTML content
    css_styles = models.TextField(blank=True)  # Custom CSS
    javascript_code = models.TextField(blank=True)  # Custom JS
    
    # SEO
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    
    # Settings
    is_published = models.BooleanField(default=False)
    is_homepage = models.BooleanField(default=False)
    requires_auth = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'title']
        unique_together = ['website', 'slug']
    
    def __str__(self):
        return f"{self.website.name} - {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Component(models.Model):
    """
    Reusable components that can be used in pages.
    """
    COMPONENT_TYPES = [
        ('header', 'Header'),
        ('footer', 'Footer'),
        ('navbar', 'Navigation Bar'),
        ('hero', 'Hero Section'),
        ('features', 'Features Section'),
        ('testimonials', 'Testimonials'),
        ('contact_form', 'Contact Form'),
        ('gallery', 'Image Gallery'),
        ('text_block', 'Text Block'),
        ('custom', 'Custom Component'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='components')
    
    name = models.CharField(max_length=100)
    component_type = models.CharField(max_length=20, choices=COMPONENT_TYPES)
    description = models.TextField(blank=True)
    
    # Content
    html_content = models.TextField()
    css_styles = models.TextField(blank=True)
    javascript_code = models.TextField(blank=True)
    
    # Settings
    is_global = models.BooleanField(default=False)  # Available across all pages
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.website.name} - {self.name}"


class Navigation(models.Model):
    """
    Navigation menu structure for websites.
    """
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='navigation_items')
    
    label = models.CharField(max_length=50)
    url = models.CharField(max_length=200)  # Can be internal page or external URL
    page = models.ForeignKey(Page, on_delete=models.CASCADE, null=True, blank=True)
    
    # Hierarchy
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    order = models.IntegerField(default=0)
    
    # Settings
    is_active = models.BooleanField(default=True)
    opens_in_new_tab = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['order', 'label']
    
    def __str__(self):
        return f"{self.website.name} - {self.label}"


class ContactForm(models.Model):
    """
    Contact form submissions from website visitors.
    """
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='contact_submissions')
    
    # Visitor information
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=100, blank=True)
    
    # Message
    subject = models.CharField(max_length=200)
    message = models.TextField()
    
    # Tracking
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    referrer = models.URLField(blank=True)
    
    # Status
    is_read = models.BooleanField(default=False)
    is_spam = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Contact from {self.name} - {self.website.name}"


class WebsiteAnalytics(models.Model):
    """
    Basic analytics tracking for websites.
    """
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='analytics')
    
    # Date tracking
    date = models.DateField()
    
    # Metrics
    page_views = models.IntegerField(default=0)
    unique_visitors = models.IntegerField(default=0)
    bounce_rate = models.FloatField(default=0.0)
    avg_session_duration = models.IntegerField(default=0)  # in seconds
    
    # Traffic sources
    organic_traffic = models.IntegerField(default=0)
    direct_traffic = models.IntegerField(default=0)
    referral_traffic = models.IntegerField(default=0)
    social_traffic = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['website', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.website.name} - {self.date}"
