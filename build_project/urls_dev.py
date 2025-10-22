"""
Simplified URL configuration for development testing
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import landing_page, api_status

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='home'),
    path('api/status/', api_status, name='api_status'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)