from django.db import models
from django_tenants.models import TenantMixin, DomainMixin


class Client(TenantMixin):
    """
    Tenant model representing each customer's isolated environment.
    Each client gets their own database schema.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    
    # Business information
    business_name = models.CharField(max_length=200)
    business_type = models.CharField(max_length=100, blank=True)
    contact_email = models.EmailField()
    
    # Subscription information
    is_active = models.BooleanField(default=True)
    subscription_plan = models.CharField(
        max_length=50, 
        choices=[
            ('starter', 'Starter'),
            ('professional', 'Professional'),
            ('enterprise', 'Enterprise'),
        ],
        default='starter'
    )
    subscription_expires = models.DateTimeField(null=True, blank=True)
    
    # Features enabled
    ai_tools_enabled = models.BooleanField(default=False)
    custom_domain_enabled = models.BooleanField(default=False)
    advanced_analytics_enabled = models.BooleanField(default=False)
    
    # Usage limits
    max_pages = models.IntegerField(default=10)
    max_storage_mb = models.IntegerField(default=1000)  # 1GB default
    max_monthly_ai_requests = models.IntegerField(default=100)
    
    # Tenant customization
    primary_color = models.CharField(max_length=7, default='#007bff')  # Hex color
    secondary_color = models.CharField(max_length=7, default='#6c757d')  # Hex color
    logo_url = models.URLField(blank=True)
    
    auto_create_schema = True
    
    class Meta:
        db_table = 'public_client'
    
    def __str__(self):
        return f"{self.name} ({self.business_name})"
    
    @property
    def is_subscription_active(self):
        """Check if the subscription is currently active."""
        if not self.subscription_expires:
            return self.is_active
        from django.utils import timezone
        return self.is_active and self.subscription_expires > timezone.now()


class Domain(DomainMixin):
    """
    Domain model for mapping subdomains to tenants.
    Each tenant can have multiple domains (e.g., custom domain + subdomain).
    """
    pass

    class Meta:
        db_table = 'public_domain'
