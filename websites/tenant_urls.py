from django.urls import path, include
from . import views

app_name = 'websites_tenant'

# Public website URLs - these serve the actual tenant websites
urlpatterns = [
    path('', views.TenantHomeView.as_view(), name='home'),
    path('contact/', views.TenantContactView.as_view(), name='contact'),
    # Include public account URLs for signup wizard access
    path('', include('accounts.public_urls')),
    path('<slug:page_slug>/', views.TenantPageView.as_view(), name='page'),
]