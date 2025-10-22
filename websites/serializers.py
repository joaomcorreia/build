from rest_framework import serializers
from .models import Website, Page, Component, Navigation, ContactForm, WebsiteAnalytics

class WebsiteSerializer(serializers.ModelSerializer):
    """Serializer for Website model"""
    
    class Meta:
        model = Website
        fields = ['id', 'name', 'description', 'domain', 'subdomain', 'theme', 
                 'custom_css', 'custom_js', 'is_published', 'seo_title', 
                 'seo_description', 'seo_keywords', 'favicon', 'logo', 
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class PageSerializer(serializers.ModelSerializer):
    """Serializer for Page model"""
    
    class Meta:
        model = Page
        fields = ['id', 'website', 'title', 'slug', 'content', 'meta_title', 
                 'meta_description', 'meta_keywords', 'is_homepage', 
                 'is_published', 'order', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class ComponentSerializer(serializers.ModelSerializer):
    """Serializer for Component model"""
    
    class Meta:
        model = Component
        fields = ['id', 'page', 'component_type', 'content', 'styles', 
                 'order', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class NavigationSerializer(serializers.ModelSerializer):
    """Serializer for Navigation model"""
    
    class Meta:
        model = Navigation
        fields = ['id', 'website', 'name', 'url', 'target', 'parent', 
                 'order', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class ContactFormSerializer(serializers.ModelSerializer):
    """Serializer for ContactForm model"""
    
    class Meta:
        model = ContactForm
        fields = ['id', 'website', 'name', 'email', 'subject', 'message', 
                 'is_read', 'created_at']
        read_only_fields = ['id', 'created_at']

class WebsiteAnalyticsSerializer(serializers.ModelSerializer):
    """Serializer for WebsiteAnalytics model"""
    
    class Meta:
        model = WebsiteAnalytics
        fields = ['id', 'website', 'page_views', 'unique_visitors', 
                 'bounce_rate', 'avg_session_duration', 'date', 'created_at']
        read_only_fields = ['id', 'created_at']