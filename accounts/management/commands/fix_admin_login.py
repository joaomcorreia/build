from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Fix admin login - delete and recreate admin user'
    
    def handle(self, *args, **options):
        # Delete existing admin users
        User.objects.filter(username='admin').delete()
        User.objects.filter(email='admin@build.platform').delete()
        
        self.stdout.write('🗑️ Deleted existing admin users')
        
        # Create fresh admin user  
        user = User.objects.create_user(
            username='admin',
            email='admin@example.com', 
            password='admin',
            first_name='Admin',
            last_name='User'
        )
        
        # Make superuser
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        
        self.stdout.write(
            self.style.SUCCESS('✅ Created fresh admin user')
        )
        self.stdout.write('=' * 40)
        self.stdout.write('🔑 NEW LOGIN CREDENTIALS:')
        self.stdout.write(f'   Username: admin')  
        self.stdout.write(f'   Password: admin')
        self.stdout.write(f'   URL: http://localhost:8000/admin/')
        self.stdout.write('=' * 40)
        
        # Verify it works
        from django.contrib.auth import authenticate
        test_user = authenticate(username='admin', password='admin')
        if test_user:
            self.stdout.write(self.style.SUCCESS('✅ Login test PASSED'))
        else:
            self.stdout.write(self.style.ERROR('❌ Login test FAILED'))
            
        self.stdout.write(
            self.style.WARNING('\n💡 Make sure to use exactly: admin / admin')
        )