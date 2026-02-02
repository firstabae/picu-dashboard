"""
Management command to create a default admin user
"""
from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = 'Create a default admin user'

    def add_arguments(self, parser):
        parser.add_argument('--email', default='admin@picu.com', help='Admin email')
        parser.add_argument('--password', default='admin123', help='Admin password')
        parser.add_argument('--name', default='Admin PICU', help='Admin full name')

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']
        name = options['name']
        
        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(f'User {email} already exists')
            )
            return
        
        user = User.objects.create_superuser(
            email=email,
            password=password,
            full_name=name,
            phone='08123456789',
        )
        user.role = 'admin'
        user.save()
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Created admin user: {email}')
        )
        self.stdout.write(f'   Password: {password}')
