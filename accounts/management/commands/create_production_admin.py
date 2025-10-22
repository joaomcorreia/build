from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = 'Create production admin user'

    def handle(self, *args, **options):
        email = 'admin@build.justcodeworks.eu'
        password = 'admin123'
        
        # Delete existing user if exists
        User.objects.filter(email=email).delete()
        
        # Create new admin user
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name='Admin',
            last_name='User'
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created admin user: {email}')
        )