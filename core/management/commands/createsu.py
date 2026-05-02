from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create superuser automatically'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                password='admin123',
                email='admin@test.com'
            )
            self.stdout.write(self.style.SUCCESS('Superuser creado'))
        else:
            self.stdout.write('Superuser ya existe')