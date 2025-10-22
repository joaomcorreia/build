from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# API routes
router = DefaultRouter()
router.register(r'websites', views.WebsiteViewSet)
router.register(r'pages', views.PageViewSet)
router.register(r'components', views.ComponentViewSet)
router.register(r'navigation', views.NavigationViewSet)
router.register(r'contact-forms', views.ContactFormViewSet)
router.register(r'analytics', views.WebsiteAnalyticsViewSet)

app_name = 'websites'

urlpatterns = [
    path('', include(router.urls)),
    path('publish/<uuid:website_id>/', views.PublishWebsiteView.as_view(), name='publish_website'),
    path('preview/<uuid:website_id>/', views.PreviewWebsiteView.as_view(), name='preview_website'),
]