from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a superuser for development'
    
    def handle(self, *args, **options):
        # Check if admin user already exists
        if User.objects.filter(username='admin').exists():
            self.stdout.write(
                self.style.WARNING('Admin user already exists')
            )
            user = User.objects.get(username='admin')
            self.stdout.write(f'Email: {user.email}')
            return
        
        # Create admin user
        user = User.objects.create_superuser(
            username='admin',
            email='admin@build.platform',
            password='admin123',
            first_name='Admin',
            last_name='User'
        )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created admin user')
        )
        self.stdout.write(f'Username: admin')
        self.stdout.write(f'Email: admin@build.platform')
        self.stdout.write(f'Password: admin123')
        self.stdout.write(
            self.style.WARNING('\n⚠️  Remember to change the password in production!')
        )