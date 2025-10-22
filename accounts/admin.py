from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserTenantRole, Subscription, APIUsage


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined']
    list_filter = ['is_staff', 'is_active', 'date_joined', 'email_verified']
    search_fields = ['email', 'first_name', 'last_name', 'company']
    ordering = ['email']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone', 'company', 'job_title')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Marketing', {'fields': ('email_verified', 'newsletter_subscription', 'marketing_emails')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name'),
        }),
    )


@admin.register(UserTenantRole)
class UserTenantRoleAdmin(admin.ModelAdmin):
    list_display = ['user', 'tenant_id', 'role', 'is_active', 'created_at']
    list_filter = ['role', 'is_active', 'created_at']
    search_fields = ['user__email', 'tenant_id']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'tenant_id', 'plan', 'status', 'started_at', 'expires_at']
    list_filter = ['plan', 'status', 'started_at']
    search_fields = ['user__email', 'tenant_id']
    readonly_fields = ['stripe_subscription_id', 'started_at']


@admin.register(APIUsage)
class APIUsageAdmin(admin.ModelAdmin):
    list_display = ['tenant_id', 'user', 'ai_requests_count', 'storage_used_mb', 'period_start', 'period_end']
    list_filter = ['period_start', 'period_end']
    search_fields = ['tenant_id', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
