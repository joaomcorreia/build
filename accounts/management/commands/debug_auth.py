from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class Command(BaseCommand):
    help = 'Debug user authentication'
    
    def handle(self, *args, **options):
        # Check what User model we're using
        self.stdout.write(f'User model: {User}')
        self.stdout.write(f'User fields: {[f.name for f in User._meta.fields]}')
        
        # List existing users
        users = User.objects.all()
        self.stdout.write(f'\nExisting users: {users.count()}')
        for user in users:
            self.stdout.write(f'  - {user.username} ({user.email}) - staff: {user.is_staff}, super: {user.is_superuser}')
        
        # Create very simple superuser
        try:
            if User.objects.filter(username='test').exists():
                User.objects.filter(username='test').delete()
                
            user = User.objects.create_superuser(
                username='test',
                email='test@test.com',
                password='test',
                first_name='Test',  # Required by our custom model
                last_name='User'    # Required by our custom model
            )
            self.stdout.write(f'✅ Created test user: {user}')
            
            # Test authentication
            auth_user = authenticate(username='test', password='test')
            self.stdout.write(f'Auth test result: {auth_user}')
            
            if auth_user:
                self.stdout.write(self.style.SUCCESS('🎉 Authentication works!'))
                self.stdout.write('=' * 40)
                self.stdout.write('🔑 WORKING CREDENTIALS:')
                self.stdout.write('   Username: test')
                self.stdout.write('   Password: test')
                self.stdout.write('   URL: http://localhost:8000/admin/')
                self.stdout.write('=' * 40)
            else:
                self.stdout.write(self.style.ERROR('❌ Authentication failed'))
                
        except Exception as e:
            self.stdout.write(f'Error: {e}')