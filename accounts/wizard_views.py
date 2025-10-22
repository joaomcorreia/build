from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth import login
from django.http import JsonResponse
from .wizard_forms import Step1PersonalForm, Step2BusinessForm, Step3DomainForm, Step4PreviewForm
from .models import User
import json
import random


class SignupWizardView(TemplateView):
    """Multi-step signup wizard"""
    template_name = 'accounts/wizard_step.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        step = int(self.kwargs.get('step', 1))
        
        # Initialize session data if not exists
        if 'wizard_data' not in self.request.session:
            self.request.session['wizard_data'] = {}
        
        context.update({
            'current_step': step,
            'total_steps': 4,
            'progress_percentage': (step / 4) * 100,
        })
        
        # Step-specific context
        if step == 1:
            context.update({
                'title': 'Welcome! Let\'s Get Started',
                'subtitle': 'Create your account to begin building your website',
                'form': Step1PersonalForm(),
                'step_icon': 'person-circle',
                'step_title': 'Personal Information'
            })
        elif step == 2:
            context.update({
                'title': 'Tell Us About Your Business',
                'subtitle': 'Help us understand your business to create the perfect website',
                'form': Step2BusinessForm(),
                'step_icon': 'building',
                'step_title': 'Business Details'
            })
        elif step == 3:
            # Generate AI-suggested domains
            wizard_data = self.request.session.get('wizard_data', {})
            business_name = wizard_data.get('business_name', '')
            business_category = wizard_data.get('business_category', '')
            
            suggested_domains = self.generate_domain_suggestions(business_name, business_category)
            
            context.update({
                'title': 'Choose Your Perfect Domain',
                'subtitle': 'We\'ve suggested some great domain names for your business',
                'form': Step3DomainForm(),
                'step_icon': 'globe',
                'step_title': 'Domain Selection',
                'suggested_domains': suggested_domains,
                'business_name': business_name
            })
        elif step == 4:
            # Generate AI preview
            wizard_data = self.request.session.get('wizard_data', {})
            ai_preview = self.generate_ai_preview(wizard_data)
            
            context.update({
                'title': 'Preview Your Website',
                'subtitle': 'Here\'s what we\'ve created for you using AI',
                'form': Step4PreviewForm(),
                'step_icon': 'eye',
                'step_title': 'AI Preview',
                'ai_preview': ai_preview,
                'wizard_data': wizard_data
            })
        
        return context
    
    def post(self, request, **kwargs):
        step = int(kwargs.get('step', 1))
        print(f"DEBUG: POST request for step {step}")
        wizard_data = request.session.get('wizard_data', {})
        
        if step == 1:
            form = Step1PersonalForm(request.POST)
            print(f"DEBUG: Step 1 form data: {request.POST}")
            print(f"DEBUG: Step 1 form valid: {form.is_valid()}")
            if not form.is_valid():
                print(f"DEBUG: Form errors: {form.errors}")
            if form.is_valid():
                # Save form data to session
                wizard_data.update({
                    'first_name': form.cleaned_data['first_name'],
                    'last_name': form.cleaned_data['last_name'],
                    'email': form.cleaned_data['email'],
                    'password1': form.cleaned_data['password1'],
                    'password2': form.cleaned_data['password2'],
                })
                request.session['wizard_data'] = wizard_data
                return redirect('accounts_public:signup_wizard', step=2)
        
        elif step == 2:
            form = Step2BusinessForm(request.POST)
            if form.is_valid():
                wizard_data.update({
                    'business_name': form.cleaned_data['business_name'],
                    'business_category': form.cleaned_data['business_category'],
                    'business_description': form.cleaned_data['business_description'],
                    'street_address': form.cleaned_data['street_address'],
                    'city': form.cleaned_data['city'],
                    'state': form.cleaned_data['state'],
                    'zip_code': form.cleaned_data['zip_code'],
                    'country': form.cleaned_data['country'],
                    'phone': form.cleaned_data['phone'],
                })
                request.session['wizard_data'] = wizard_data
                return redirect('accounts_public:signup_wizard', step=3)
        
        elif step == 3:
            form = Step3DomainForm(request.POST)
            if form.is_valid():
                wizard_data.update({
                    'selected_domain': form.cleaned_data['selected_domain'],
                    'custom_domain': form.cleaned_data['custom_domain'],
                })
                request.session['wizard_data'] = wizard_data
                return redirect('accounts_public:signup_wizard', step=4)
        
        elif step == 4:
            form = Step4PreviewForm(request.POST)
            if form.is_valid():
                # Create the user account
                user_data = wizard_data
                user = User.objects.create_user(
                    username=user_data['email'],
                    email=user_data['email'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    company=user_data['business_name']
                )
                user.set_password(user_data['password1'])
                user.save()
                
                # Save all wizard data for website creation
                wizard_data.update({
                    'design_style': form.cleaned_data['design_style'],
                    'color_scheme': form.cleaned_data['color_scheme'],
                    'additional_requests': form.cleaned_data['additional_requests'],
                })
                
                # Store complete data for website creation
                request.session['website_creation_data'] = wizard_data
                
                # Login the user
                login(request, user)
                
                messages.success(request, f'Welcome {user.first_name}! Your account has been created.')
                return redirect('accounts_public:website_creation_success')
        
        # If we get here, form validation failed
        messages.error(request, 'Please correct the errors below.')
        
        # Re-render the current step with the form errors
        context = self.get_context_data(**kwargs)
        
        # Make sure we pass the form with errors for the current step
        if step == 1:
            context['form'] = Step1PersonalForm(request.POST)
            context.update({
                'title': 'Welcome! Let\'s Get Started',
                'subtitle': 'Create your account to begin building your website',
                'step_icon': 'person-circle',
                'step_title': 'Personal Information'
            })
        elif step == 2:
            context['form'] = Step2BusinessForm(request.POST)
            context.update({
                'title': 'Tell Us About Your Business',
                'subtitle': 'Help us understand your business to create the perfect website',
                'step_icon': 'building',
                'step_title': 'Business Details'
            })
        elif step == 3:
            context['form'] = Step3DomainForm(request.POST)
            context.update({
                'title': 'Choose Your Perfect Domain',
                'subtitle': 'We\'ve suggested some great domain names for your business',
                'step_icon': 'globe',
                'step_title': 'Domain Selection'
            })
        elif step == 4:
            context['form'] = Step4PreviewForm(request.POST)
            context.update({
                'title': 'Preview Your Website',
                'subtitle': 'Here\'s what we\'ve created for you using AI',
                'step_icon': 'eye',
                'step_title': 'AI Preview'
            })
        
        return render(request, self.template_name, context)
    
    def generate_domain_suggestions(self, business_name, category):
        """Generate AI-powered domain suggestions"""
        suggestions = []
        
        if business_name:
            # Clean business name for domain
            clean_name = ''.join(e for e in business_name.lower() if e.isalnum())
            
            # Base suggestions
            base_suggestions = [
                f"{clean_name}.com",
                f"{clean_name}online.com",
                f"{clean_name}pro.com",
                f"get{clean_name}.com",
                f"{clean_name}hub.com",
            ]
            
            # Category-specific suggestions
            category_suffixes = {
                'restaurant': ['eats', 'kitchen', 'bistro', 'cafe'],
                'retail': ['shop', 'store', 'market', 'boutique'],
                'professional': ['services', 'solutions', 'consulting', 'experts'],
                'healthcare': ['health', 'care', 'medical', 'clinic'],
                'beauty': ['beauty', 'salon', 'spa', 'style'],
                'fitness': ['fitness', 'gym', 'training', 'wellness'],
            }
            
            if category in category_suffixes:
                for suffix in category_suffixes[category]:
                    suggestions.append(f"{clean_name}{suffix}.com")
            
            # Add base suggestions
            suggestions.extend(base_suggestions[:3])
            
            # Check availability (mock for now)
            domain_data = []
            for domain in suggestions[:6]:
                domain_data.append({
                    'domain': domain,
                    'available': random.choice([True, False]),  # Mock availability
                    'price': random.choice(['$12.99', '$15.99', '$19.99']),
                    'recommended': len(domain_data) < 2  # First 2 are recommended
                })
        
        return domain_data
    
    def generate_ai_preview(self, wizard_data):
        """Generate AI-powered website preview content"""
        business_name = wizard_data.get('business_name', 'Your Business')
        category = wizard_data.get('business_category', 'business')
        description = wizard_data.get('business_description', '')
        location = f"{wizard_data.get('city', '')}, {wizard_data.get('state', '')}"
        
        # AI-generated content based on category
        category_content = {
            'restaurant': {
                'headline': f"Welcome to {business_name}",
                'tagline': "Delicious food, unforgettable experiences",
                'services': ["Fine Dining", "Takeout & Delivery", "Catering", "Private Events"],
                'about': f"{business_name} brings you the finest culinary experience in {location}. Our passionate chefs create memorable dishes using the freshest ingredients."
            },
            'professional': {
                'headline': f"Professional Excellence at {business_name}",
                'tagline': "Your trusted partner for success",
                'services': ["Consulting", "Strategic Planning", "Expert Analysis", "Custom Solutions"],
                'about': f"{business_name} provides top-tier professional services in {location}. We help businesses achieve their goals with expert guidance and proven strategies."
            },
            'retail': {
                'headline': f"Shop the Best at {business_name}",
                'tagline': "Quality products, exceptional service",
                'services': ["Online Shopping", "In-Store Experience", "Customer Support", "Fast Delivery"],
                'about': f"{business_name} is your premier shopping destination in {location}. We offer carefully curated products and outstanding customer service."
            },
            # Add more categories as needed
        }
        
        # Default content
        default_content = {
            'headline': f"Welcome to {business_name}",
            'tagline': "Excellence in everything we do",
            'services': ["Quality Service", "Expert Team", "Customer Focus", "Reliable Solutions"],
            'about': f"{business_name} is a trusted business serving {location}. We pride ourselves on delivering exceptional service and building lasting relationships with our customers."
        }
        
        content = category_content.get(category, default_content)
        
        # Add user description if provided
        if description:
            content['about'] = description
        
        return content


class WebsiteCreationSuccessView(TemplateView):
    """Success page after wizard completion"""
    template_name = 'accounts/creation_success.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wizard_data = self.request.session.get('website_creation_data', {})
        
        context.update({
            'title': f'{wizard_data.get("business_name", "Your Website")} is Being Created!',
            'subtitle': 'We\'re setting up your professional website with AI-generated content.',
            'business_name': wizard_data.get('business_name', 'Your Business'),
            'domain': wizard_data.get('selected_domain', 'your-domain.com'),
            'wizard_data': wizard_data
        })
        
        return context