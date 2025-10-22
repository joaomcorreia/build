from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'clients', views.ClientViewSet)
router.register(r'domains', views.DomainViewSet)

app_name = 'tenants'

urlpatterns = [
    path('', include(router.urls)),
    path('create/', views.CreateTenantView.as_view(), name='create_tenant'),
    path('switch/<str:tenant_id>/', views.SwitchTenantView.as_view(), name='switch_tenant'),
]