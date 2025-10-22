from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import APIView
from .forms import CompanySignUpForm


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


class LandingPageView(TemplateView):
    template_name = 'accounts/landing.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Build Platform - Multi-Tenant Website Builder',
            'description': 'Create and manage websites with AI-powered tools',
            'features': [
                'Multi-tenant architecture',
                'AI-powered content generation', 
                'Advanced media management',
                'Responsive website builder',
                'SEO optimization tools',
            ]
        })
        return context

class SignUpView(CreateView):
    form_class = CompanySignUpForm
    template_name = 'accounts/signup.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Start Building Your Website',
            'subtitle': 'Create your account and get started in minutes',
        })
        return context
    
    def form_valid(self, form):
        # Save the user
        user = form.save()
        
        # Store website details in session for later use
        website_data = {
            'website_name': form.cleaned_data['website_name'],
            'website_type': form.cleaned_data['website_type'],
            'desired_domain': form.cleaned_data['desired_domain'],
        }
        self.request.session['website_data'] = website_data
        
        messages.success(
            self.request, 
            f'Welcome {user.first_name}! Your account has been created successfully.'
        )
        
        # Redirect to website configuration or payment
        return redirect('accounts_public:website_setup')
    
    def form_invalid(self, form):
        messages.error(
            self.request,
            'Please correct the errors below and try again.'
        )
        return super().form_invalid(form)

class WebsiteSetupView(TemplateView):
    template_name = 'accounts/website_setup.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        website_data = self.request.session.get('website_data', {})
        context.update({
            'title': 'Configure Your Website',
            'subtitle': 'Let\'s set up your website details',
            'website_data': website_data
        })
        return context

class PricingView(TemplateView):
    template_name = 'accounts/pricing.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Pricing',
            'plans': [
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
        })
        return context

class FeaturesView(TemplateView):
    template_name = 'accounts/features.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Features'
        return context

class ContactView(TemplateView):
    template_name = 'accounts/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Contact'
        return context


class AboutView(TemplateView):
    template_name = 'accounts/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'About'
        return context

class PublicLoginView(TemplateView):
    template_name = 'accounts/login.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context


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
