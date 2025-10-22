from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
import requests


class Step1PersonalForm(UserCreationForm):
    """Step 1: Personal Information"""
    
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'First Name',
            'autofocus': True
        })
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Last Name'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Your Email Address'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Create Password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Confirm Password'
        })
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']


class Step2BusinessForm(forms.Form):
    """Step 2: Business Information"""
    
    BUSINESS_CATEGORIES = [
        ('restaurant', 'Restaurant & Food Service'),
        ('retail', 'Retail & E-commerce'),
        ('professional', 'Professional Services'),
        ('healthcare', 'Healthcare & Medical'),
        ('beauty', 'Beauty & Wellness'),
        ('fitness', 'Fitness & Sports'),
        ('education', 'Education & Training'),
        ('technology', 'Technology & Software'),
        ('consulting', 'Consulting & Coaching'),
        ('real_estate', 'Real Estate'),
        ('automotive', 'Automotive'),
        ('construction', 'Construction & Home Services'),
        ('finance', 'Finance & Insurance'),
        ('legal', 'Legal Services'),
        ('marketing', 'Marketing & Advertising'),
        ('photography', 'Photography & Creative'),
        ('travel', 'Travel & Tourism'),
        ('nonprofit', 'Non-Profit Organization'),
        ('event', 'Event Planning'),
        ('other', 'Other'),
    ]
    
    business_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Your Business Name'
        })
    )
    
    business_category = forms.ChoiceField(
        choices=BUSINESS_CATEGORIES,
        widget=forms.Select(attrs={
            'class': 'form-control form-control-lg'
        })
    )
    
    business_description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Brief description of your business (optional)',
            'rows': 3
        })
    )
    
    # Address fields
    street_address = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Street Address'
        })
    )
    
    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'City'
        })
    )
    
    state = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'State/Province'
        })
    )
    
    zip_code = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ZIP/Postal Code'
        })
    )
    
    country = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Country',
            'value': 'United States'
        })
    )
    
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Business Phone (optional)'
        })
    )

    def clean_street_address(self):
        """Validate address using a geocoding service"""
        address = self.cleaned_data.get('street_address')
        city = self.cleaned_data.get('city')
        state = self.cleaned_data.get('state')
        
        if address and city and state:
            # You can integrate with Google Maps API or similar for validation
            # For now, we'll do basic validation
            full_address = f"{address}, {city}, {state}"
            if len(full_address.strip()) < 10:
                raise forms.ValidationError("Please provide a complete address")
        
        return address


class Step3DomainForm(forms.Form):
    """Step 3: Domain Selection"""
    
    selected_domain = forms.CharField(
        widget=forms.HiddenInput()
    )
    
    custom_domain = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your own domain idea'
        })
    )


class Step4PreviewForm(forms.Form):
    """Step 4: AI Preview Confirmation"""
    
    DESIGN_CHOICES = [
        ('modern', 'Modern & Clean'),
        ('professional', 'Professional & Corporate'),
        ('creative', 'Creative & Artistic'),
        ('minimal', 'Minimal & Simple'),
        ('bold', 'Bold & Vibrant'),
    ]
    
    COLOR_CHOICES = [
        ('blue', 'Blue & White'),
        ('green', 'Green & Natural'),
        ('purple', 'Purple & Elegant'),
        ('orange', 'Orange & Energetic'),
        ('dark', 'Dark & Professional'),
        ('custom', 'Custom Colors'),
    ]
    
    approve_content = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    design_style = forms.ChoiceField(
        choices=DESIGN_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input'
        })
    )
    
    color_scheme = forms.ChoiceField(
        choices=COLOR_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input'
        })
    )
    
    additional_requests = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Any specific requests or changes you\'d like to make?',
            'rows': 3
        })
    )