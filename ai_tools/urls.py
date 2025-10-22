from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# API routes
router = DefaultRouter()
router.register(r'tools', views.AIToolViewSet)
router.register(r'requests', views.AIRequestViewSet)
router.register(r'templates', views.ContentTemplateViewSet)
router.register(r'generated-content', views.GeneratedContentViewSet)

app_name = 'ai_tools'

urlpatterns = [
    path('', include(router.urls)),
    path('generate-content/', views.GenerateContentView.as_view(), name='generate_content'),
    path('generate-image/', views.GenerateImageView.as_view(), name='generate_image'),
    path('optimize-seo/', views.OptimizeSEOView.as_view(), name='optimize_seo'),
    path('improve-text/', views.ImproveTextView.as_view(), name='improve_text'),
    path('usage-stats/', views.AIUsageStatsView.as_view(), name='usage_stats'),
    path('configuration/', views.AIConfigurationView.as_view(), name='configuration'),
]