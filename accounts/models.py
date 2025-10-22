from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """
    Extended user model for the platform.
    This is stored in the public schema and shared across all tenants.
    """
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    
    # Profile information
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    
    # Account settings
    email_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)
    
    # Marketing preferences
    newsletter_subscription = models.BooleanField(default=False)
    marketing_emails = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        db_table = 'public_user'
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()


class UserTenantRole(models.Model):
    """
    Defines user roles within specific tenants.
    A user can have different roles in different tenants.
    """
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('admin', 'Administrator'),
        ('editor', 'Editor'),
        ('viewer', 'Viewer'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tenant_id = models.CharField(max_length=100)  # Schema name of the tenant
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'public_user_tenant_role'
        unique_together = ['user', 'tenant_id']
    
    def __str__(self):
        return f"{self.user.email} - {self.role} in {self.tenant_id}"


class Subscription(models.Model):
    """
    Subscription model linking users to tenant subscriptions.
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('canceled', 'Canceled'),
        ('expired', 'Expired'),
        ('suspended', 'Suspended'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tenant_id = models.CharField(max_length=100)  # Schema name of the tenant
    plan = models.CharField(max_length=50, choices=[
        ('starter', 'Starter - $9/month'),
        ('professional', 'Professional - $29/month'),
        ('enterprise', 'Enterprise - $99/month'),
    ])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Billing information
    started_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    next_billing_date = models.DateTimeField()
    
    # Payment tracking
    stripe_subscription_id = models.CharField(max_length=100, blank=True)
    last_payment_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'public_subscription'
    
    def __str__(self):
        return f"{self.user.email} - {self.plan} ({self.status})"
    
    @property
    def is_active(self):
        return self.status == 'active' and self.expires_at > timezone.now()


class APIUsage(models.Model):
    """
    Track API usage for billing and rate limiting.
    """
    tenant_id = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Usage tracking
    ai_requests_count = models.IntegerField(default=0)
    storage_used_mb = models.FloatField(default=0.0)
    bandwidth_used_mb = models.FloatField(default=0.0)
    
    # Time period
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'public_api_usage'
        unique_together = ['tenant_id', 'user', 'period_start']
    
    def __str__(self):
        return f"{self.tenant_id} - {self.period_start.strftime('%Y-%m')}"
