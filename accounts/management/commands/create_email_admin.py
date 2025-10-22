from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class Command(BaseCommand):
    help = 'Create working admin with email login'
    
    def handle(self, *args, **options):
        # Delete existing users
        User.objects.all().delete()
        self.stdout.write('🗑️ Cleared all users')
        
        # Create admin user - remember USERNAME_FIELD = 'email'!
        user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',  # This is what we login with!
            password='admin',
            first_name='Admin',
            last_name='User'
        )
        
        self.stdout.write(f'✅ Created user: {user}')
        
        # Test authentication with EMAIL (not username)
        auth_user = authenticate(username='admin@test.com', password='admin')  # Use email!
        
        if auth_user:
            self.stdout.write(self.style.SUCCESS('🎉 Email authentication works!'))
            self.stdout.write('=' * 50)
            self.stdout.write('🔑 CORRECT LOGIN CREDENTIALS:')
            self.stdout.write('   Username: admin@test.com  (use EMAIL)')
            self.stdout.write('   Password: admin')
            self.stdout.write('   URL: http://localhost:8000/admin/')
            self.stdout.write('=' * 50)
            self.stdout.write(self.style.WARNING('⚠️  Login with EMAIL, not username!'))
        else:
            self.stdout.write(self.style.ERROR('❌ Still failed - checking issue'))
            
        # Also test username-based auth
        auth_user2 = authenticate(username='admin', password='admin')
        if auth_user2:
            self.stdout.write('Username auth also works')
        else:
            self.stdout.write('Username auth failed (expected)')