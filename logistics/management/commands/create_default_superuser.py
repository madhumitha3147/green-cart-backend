# backend/logistics/management/commands/create_default_superuser.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create default superuser if not exists'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('manager', 'manager@example.com', 'Madhu@31')
            self.stdout.write(self.style.SUCCESS('Default superuser created'))
        else:
            self.stdout.write('Default superuser already exists')
