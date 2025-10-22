from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from .models import Client, Domain


@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ['name', 'business_name', 'contact_email', 'subscription_plan', 'is_active', 'created_on']
    list_filter = ['subscription_plan', 'is_active', 'ai_tools_enabled', 'created_on']
    search_fields = ['name', 'business_name', 'contact_email']
    readonly_fields = ['created_on', 'schema_name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'business_name', 'description', 'contact_email')
        }),
        ('Subscription', {
            'fields': ('subscription_plan', 'subscription_expires', 'is_active')
        }),
        ('Features', {
            'fields': ('ai_tools_enabled', 'custom_domain_enabled', 'advanced_analytics_enabled')
        }),
        ('Limits', {
            'fields': ('max_pages', 'max_storage_mb', 'max_monthly_ai_requests')
        }),
        ('Customization', {
            'fields': ('primary_color', 'secondary_color', 'logo_url')
        }),
        ('System', {
            'fields': ('schema_name', 'created_on'),
            'classes': ['collapse']
        })
    )


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['domain', 'tenant', 'is_primary']
    list_filter = ['is_primary']
    search_fields = ['domain']
