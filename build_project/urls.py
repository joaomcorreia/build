"""
URL configuration for build_project - Tenant URLs

These URLs are available within tenant schemas.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/websites/', include('websites.urls')),
    path('api/v1/media/', include('media_library.urls')),
    path('api/v1/ai-tools/', include('ai_tools.urls')),
    path('', include('websites.tenant_urls')),  # Public website URLs
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
