from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from tenants.models import Client, Domain


class Command(BaseCommand):
    help = 'Create a new tenant for a customer'
    
    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Tenant name')
        parser.add_argument('domain', type=str, help='Subdomain (e.g., "customer" for customer.build.justcodeworks.eu)')
        parser.add_argument('business_name', type=str, help='Business name')
        parser.add_argument('contact_email', type=str, help='Contact email')
        
        parser.add_argument(
            '--plan',
            type=str,
            choices=['starter', 'professional', 'enterprise'],
            default='starter',
            help='Subscription plan (default: starter)'
        )
        
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Subscription duration in days (default: 30)'
        )
    
    def handle(self, *args, **options):
        name = options['name']
        domain_prefix = options['domain']
        business_name = options['business_name']
        contact_email = options['contact_email']
        plan = options['plan']
        duration_days = options['days']
        
        # Create schema name from domain prefix
        schema_name = domain_prefix.lower().replace('-', '_').replace(' ', '_')
        full_domain = f"{domain_prefix}.build.justcodeworks.eu"
        
        # Check if tenant already exists
        if Client.objects.filter(schema_name=schema_name).exists():
            self.stdout.write(
                self.style.ERROR(f'Tenant with schema "{schema_name}" already exists')
            )
            return
        
        if Domain.objects.filter(domain=full_domain).exists():
            self.stdout.write(
                self.style.ERROR(f'Domain "{full_domain}" already exists')
            )
            return
        
        # Plan configurations
        plan_configs = {
            'starter': {
                'max_pages': 10,
                'max_storage_mb': 1000,  # 1GB
                'max_monthly_ai_requests': 100,
                'ai_tools_enabled': False,
                'custom_domain_enabled': False,
                'advanced_analytics_enabled': False,
            },
            'professional': {
                'max_pages': 50,
                'max_storage_mb': 5000,  # 5GB
                'max_monthly_ai_requests': 500,
                'ai_tools_enabled': True,
                'custom_domain_enabled': True,
                'advanced_analytics_enabled': False,
            },
            'enterprise': {
                'max_pages': 200,
                'max_storage_mb': 20000,  # 20GB
                'max_monthly_ai_requests': 2000,
                'ai_tools_enabled': True,
                'custom_domain_enabled': True,
                'advanced_analytics_enabled': True,
            },
        }
        
        config = plan_configs[plan]
        
        # Create the tenant
        tenant = Client.objects.create(
            schema_name=schema_name,
            name=name,
            business_name=business_name,
            description=f'Tenant for {business_name}',
            contact_email=contact_email,
            subscription_plan=plan,
            subscription_expires=timezone.now() + timedelta(days=duration_days),
            is_active=True,
            **config
        )
        
        # Create the domain
        domain = Domain.objects.create(
            domain=full_domain,
            tenant=tenant,
            is_primary=True
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created tenant: {tenant.name}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Schema: {tenant.schema_name}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Domain: {domain.domain}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Plan: {plan} (expires: {tenant.subscription_expires})')
        )
        
        # Next steps
        self.stdout.write(
            self.style.WARNING(f'\nTo migrate the tenant schema, run:')
        )
        self.stdout.write(f'python manage.py migrate_schemas --schema={schema_name}')