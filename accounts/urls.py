from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# API routes (placeholder for now)
# router = DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'subscriptions', views.SubscriptionViewSet)

app_name = 'accounts'

urlpatterns = [
    # path('', include(router.urls)),  # Commented out for now
    path('status/', views.api_status, name='api_status'),
    # path('register/', views.RegisterView.as_view(), name='register'),
    # path('login/', views.LoginView.as_view(), name='login'),
    # path('logout/', views.LogoutView.as_view(), name='logout'),
    # path('profile/', views.ProfileView.as_view(), name='profile'),
    # path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    # path('reset-password/', views.ResetPasswordView.as_view(), name='reset_password'),
]