from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from customerleads.models import UserProfile

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds default admin/superuser and developer credentials'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@auresancrm.com',
                password='Admin@123',
                first_name='System',
                last_name='Administrator',
            )
            UserProfile.objects.create(
                user=admin,
                role='admin',
                phone='+256700000000',
                department='IT',
                bio='Default developer admin account. Change password in production.',
            )
            self.stdout.write(self.style.SUCCESS('Default admin user created successfully.'))
            self.stdout.write(self.style.WARNING('Username: admin'))
            self.stdout.write(self.style.WARNING('Password: Admin@123'))
            self.stdout.write(self.style.WARNING('IMPORTANT: Change these credentials in production!'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists. Skipping seed.'))

        if not User.objects.filter(username='developer').exists():
            developer = User.objects.create_user(
                username='developer',
                email='developer@auresancrm.com',
                password='Dev@123',
                first_name='Developer',
                last_name='Account',
                is_staff=True,
            )
            UserProfile.objects.create(
                user=developer,
                role='admin',
                phone='+256700000001',
                department='Development',
                bio='Default developer account for testing.',
            )
            self.stdout.write(self.style.SUCCESS('Default developer user created successfully.'))
            self.stdout.write(self.style.WARNING('Username: developer'))
            self.stdout.write(self.style.WARNING('Password: Dev@123'))
            self.stdout.write(self.style.WARNING('IMPORTANT: Change these credentials in production!'))
        else:
            self.stdout.write(self.style.WARNING('Developer user already exists. Skipping seed.'))
