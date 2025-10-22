"""
Public URLs for the main domain (build.justcodeworks.eu)

These URLs are available on the public schema before tenant selection.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from accounts.views import api_status

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/status/', api_status, name='api_status'),  # Direct API status endpoint
    path('api/v1/auth/', include('accounts.urls')),
    path('api/v1/tenants/', include('tenants.urls')),
    path('', include('accounts.public_urls')),  # Landing page, signup, login
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)