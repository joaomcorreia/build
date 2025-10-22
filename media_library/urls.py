from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# API routes
router = DefaultRouter()
router.register(r'files', views.MediaFileViewSet)
router.register(r'folders', views.MediaFolderViewSet)
router.register(r'optimizations', views.ImageOptimizationViewSet)

app_name = 'media_library'

urlpatterns = [
    path('', include(router.urls)),
    path('upload/', views.MediaUploadView.as_view(), name='upload'),
    path('bulk-upload/', views.BulkUploadView.as_view(), name='bulk_upload'),
    path('optimize/<uuid:file_id>/', views.OptimizeImageView.as_view(), name='optimize_image'),
    path('settings/', views.MediaLibrarySettingsView.as_view(), name='settings'),
]