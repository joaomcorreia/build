from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Check admin user and reset password if needed'
    
    def handle(self, *args, **options):
        try:
            user = User.objects.get(username='admin')
            self.stdout.write(f'✅ Admin user found: {user.username} ({user.email})')
            
            # Reset password to be sure
            user.set_password('admin123')
            user.save()
            
            self.stdout.write(
                self.style.SUCCESS('✅ Password reset to: admin123')
            )
            
            # Check if user is staff and superuser
            if not user.is_staff:
                user.is_staff = True
                user.save()
                self.stdout.write('✅ Made user staff')
                
            if not user.is_superuser:
                user.is_superuser = True  
                user.save()
                self.stdout.write('✅ Made user superuser')
                
            self.stdout.write(
                self.style.SUCCESS('\n🎉 Admin user ready!')
            )
            self.stdout.write('Username: admin')
            self.stdout.write('Password: admin123')
            self.stdout.write('URL: http://localhost:8000/admin/')
            
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('❌ Admin user not found. Run create_dev_admin first.')
            )