import os
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Initialize tenant database with proper migrations'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force initialization even if tables exist',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting tenant database initialization...'))
        
        try:
            # Step 1: Migrate shared apps (creates public schema and tenant table)
            self.stdout.write('Step 1: Migrating shared apps...')
            call_command('migrate_schemas', '--shared')
            
            # Step 2: Create public tenant if it doesn't exist
            self.stdout.write('Step 2: Creating public tenant...')
            from tenants.models import Client
            
            public_tenant, created = Client.objects.get_or_create(
                schema_name='public',
                defaults={
                    'name': 'System',
                    'domain_url': 'localhost',
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS('✓ Public tenant created'))
            else:
                self.stdout.write(self.style.WARNING('Public tenant already exists'))
            
            # Step 3: Run migrations for tenant apps
            self.stdout.write('Step 3: Migrating tenant apps...')
            call_command('migrate_schemas', '--tenant')
            
            # Step 4: Run standard migrations
            self.stdout.write('Step 4: Running standard migrations...')
            call_command('migrate')
            
            self.stdout.write(self.style.SUCCESS('✅ Tenant database initialization complete!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error during initialization: {e}'))
            raise e