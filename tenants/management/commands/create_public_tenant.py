from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from tenants.models import Client, Domain


class Command(BaseCommand):
    help = 'Create the main public tenant for the platform'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--domain',
            type=str,
            default='build.justcodeworks.eu',
            help='The main domain for the platform (default: build.justcodeworks.eu)'
        )
        
        parser.add_argument(
            '--name',
            type=str,
            default='Build Platform',
            help='Name of the main tenant (default: Build Platform)'
        )
    
    def handle(self, *args, **options):
        domain_name = options['domain']
        tenant_name = options['name']
        
        # Check if public tenant already exists
        try:
            tenant = Client.objects.get(schema_name='public')
            self.stdout.write(
                self.style.WARNING(f'Public tenant already exists: {tenant.name}')
            )
            return
        except Client.DoesNotExist:
            pass
        
        # Create the public tenant
        tenant = Client.objects.create(
            schema_name='public',
            name=tenant_name,
            business_name='Build Platform',
            description='Main platform tenant for managing subscriptions and user accounts',
            contact_email='admin@justcodeworks.eu',
            subscription_plan='enterprise',
            is_active=True,
            ai_tools_enabled=True,
            custom_domain_enabled=True,
            advanced_analytics_enabled=True,
            max_pages=1000,
            max_storage_mb=50000,  # 50GB
            max_monthly_ai_requests=10000,
        )
        
        # Create the domain
        domain = Domain.objects.create(
            domain=domain_name,
            tenant=tenant,
            is_primary=True
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created public tenant: {tenant.name}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Domain configured: {domain.domain}')
        )
        
        # Instructions
        self.stdout.write(
            self.style.WARNING('\nNext steps:')
        )
        self.stdout.write('1. Run: python manage.py migrate_schemas')
        self.stdout.write('2. Run: python manage.py create_tenant_command')
        self.stdout.write('3. Create superuser: python manage.py createsuperuser')