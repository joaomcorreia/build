from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


def landing_page(request):
    """
    Landing page view for the main domain.
    """
    context = {
        'title': 'Build Platform - Multi-Tenant Website Builder',
        'description': 'Create and manage websites with AI-powered tools',
        'features': [
            'Multi-tenant architecture',
            'AI-powered content generation', 
            'Advanced media management',
            'Responsive website builder',
            'SEO optimization tools',
            'Subscription management'
        ]
    }
    return render(request, 'landing.html', context)


class LandingPageView:
    def as_view(self):
        return landing_page


class SignUpView:
    def as_view(self):
        def signup_view(request):
            return render(request, 'signup.html', {'title': 'Sign Up'})
        return signup_view


class PricingView:
    def as_view(self):
        def pricing_view(request):
            plans = [
                {
                    'name': 'Starter',
                    'price': '$9/month',
                    'features': ['10 pages', '1GB storage', 'Basic support']
                },
                {
                    'name': 'Professional', 
                    'price': '$29/month',
                    'features': ['50 pages', '5GB storage', 'AI tools', 'Priority support']
                },
                {
                    'name': 'Enterprise',
                    'price': '$99/month', 
                    'features': ['200 pages', '20GB storage', 'Advanced AI', 'Custom domains']
                }
            ]
            return render(request, 'pricing.html', {'title': 'Pricing', 'plans': plans})
        return pricing_view


class FeaturesView:
    def as_view(self):
        def features_view(request):
            return render(request, 'features.html', {'title': 'Features'})
        return features_view


class ContactView:
    def as_view(self):
        def contact_view(request):
            return render(request, 'contact.html', {'title': 'Contact'})
        return contact_view


class AboutView:
    def as_view(self):
        def about_view(request):
            return render(request, 'about.html', {'title': 'About'})
        return about_view


class PublicLoginView:
    def as_view(self):
        def login_view(request):
            return render(request, 'login.html', {'title': 'Login'})
        return login_view


@api_view(['GET'])
def api_status(request):
    """
    API status endpoint to test the API is working.
    """
    return Response({
        'status': 'success',
        'message': 'Build Platform API is running',
        'version': '1.0.0',
        'features': {
            'multi_tenancy': True,
            'ai_tools': True,
            'media_library': True,
            'website_builder': True
        }
    })


# Placeholder views for other ViewSets (we'll implement these later)
class UserViewSet:
    pass

class SubscriptionViewSet:
    pass

class RegisterView:
    pass

class LoginView:
    pass

class LogoutView:
    pass

class ProfileView:
    pass

class ChangePasswordView:
    pass

class ResetPasswordView:
    pass
