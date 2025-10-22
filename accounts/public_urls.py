from django.urls import path
from . import views
from . import wizard_views

app_name = 'accounts_public'

urlpatterns = [
    path('', views.LandingPageView.as_view(), name='landing'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signup-wizard/', wizard_views.SignupWizardView.as_view(), {'step': 1}, name='signup_wizard_start'),
    path('signup-wizard/<int:step>/', wizard_views.SignupWizardView.as_view(), name='signup_wizard'),
    path('website-creation-success/', wizard_views.WebsiteCreationSuccessView.as_view(), name='website_creation_success'),
    path('website-setup/', views.WebsiteSetupView.as_view(), name='website_setup'),
    path('pricing/', views.PricingView.as_view(), name='pricing'),
    path('features/', views.FeaturesView.as_view(), name='features'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('login/', views.PublicLoginView.as_view(), name='login'),
]