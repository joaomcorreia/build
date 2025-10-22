from django.urls import path
from . import views

app_name = 'websites_tenant'

# Public website URLs - these serve the actual tenant websites
urlpatterns = [
    path('', views.TenantHomeView.as_view(), name='home'),
    path('contact/', views.TenantContactView.as_view(), name='contact'),
    path('<slug:page_slug>/', views.TenantPageView.as_view(), name='page'),
]