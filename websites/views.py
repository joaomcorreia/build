from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from .models import Website, Page, Component, Navigation, ContactForm, WebsiteAnalytics
from .serializers import (
    WebsiteSerializer, PageSerializer, ComponentSerializer, 
    NavigationSerializer, ContactFormSerializer, WebsiteAnalyticsSerializer
)

class WebsiteViewSet(viewsets.ModelViewSet):
    """ViewSet for managing websites"""
    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer
    
    def get_queryset(self):
        # Filter by current tenant
        return Website.objects.filter(tenant=self.request.tenant)

class PageViewSet(viewsets.ModelViewSet):
    """ViewSet for managing pages"""
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    
    def get_queryset(self):
        # Filter by current tenant's websites
        return Page.objects.filter(website__tenant=self.request.tenant)

class ComponentViewSet(viewsets.ModelViewSet):
    """ViewSet for managing components"""
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer
    
    def get_queryset(self):
        # Filter by current tenant's pages
        return Component.objects.filter(page__website__tenant=self.request.tenant)

class NavigationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing navigation"""
    queryset = Navigation.objects.all()
    serializer_class = NavigationSerializer
    
    def get_queryset(self):
        # Filter by current tenant's websites
        return Navigation.objects.filter(website__tenant=self.request.tenant)

class ContactFormViewSet(viewsets.ModelViewSet):
    """ViewSet for managing contact forms"""
    queryset = ContactForm.objects.all()
    serializer_class = ContactFormSerializer
    
    def get_queryset(self):
        # Filter by current tenant's websites
        return ContactForm.objects.filter(website__tenant=self.request.tenant)

class WebsiteAnalyticsViewSet(viewsets.ModelViewSet):
    """ViewSet for managing website analytics"""
    queryset = WebsiteAnalytics.objects.all()
    serializer_class = WebsiteAnalyticsSerializer
    
    def get_queryset(self):
        # Filter by current tenant's websites
        return WebsiteAnalytics.objects.filter(website__tenant=self.request.tenant)

class PublishWebsiteView(APIView):
    """View for publishing websites"""
    
    def post(self, request, website_id):
        try:
            website = Website.objects.get(id=website_id, tenant=request.tenant)
            website.is_published = True
            website.save()
            return Response({'status': 'published'}, status=status.HTTP_200_OK)
        except Website.DoesNotExist:
            return Response({'error': 'Website not found'}, status=status.HTTP_404_NOT_FOUND)

class PreviewWebsiteView(APIView):
    """View for previewing websites"""
    
    def get(self, request, website_id):
        try:
            website = Website.objects.get(id=website_id, tenant=request.tenant)
            # Return preview HTML or data
            return Response({
                'website': WebsiteSerializer(website).data,
                'preview_url': f'/preview/{website_id}/'
            }, status=status.HTTP_200_OK)
        except Website.DoesNotExist:
            return Response({'error': 'Website not found'}, status=status.HTTP_404_NOT_FOUND)

# Tenant-facing views (for serving actual websites)
from django.views.generic import TemplateView

class TenantHomeView(TemplateView):
    """View for tenant website home page"""
    template_name = 'websites/tenant_home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add website data for the current tenant
        try:
            website = Website.objects.filter(tenant=self.request.tenant).first()
            context['website'] = website
        except:
            context['website'] = None
        return context

class TenantContactView(TemplateView):
    """View for tenant website contact page"""
    template_name = 'websites/tenant_contact.html'
    
    def post(self, request, *args, **kwargs):
        # Handle contact form submission
        return self.get(request, *args, **kwargs)

class TenantPageView(TemplateView):
    """View for tenant website pages"""
    template_name = 'websites/tenant_page.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_slug = kwargs.get('page_slug')
        try:
            page = Page.objects.filter(
                website__tenant=self.request.tenant, 
                slug=page_slug
            ).first()
            context['page'] = page
        except:
            context['page'] = None
        return context
