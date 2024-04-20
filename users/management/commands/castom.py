import os
from dotenv import load_dotenv
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from users.models import User


load_dotenv()


class Command(BaseCommand):
    help = 'Create a superuser with given email and password from environment'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Email for the new superuser')

    def handle(self, *args, **options):
        email = options['email'] or os.getenv('SUPERUSER_EMAIL')
        password = os.getenv('SUPERUSER_PASSWORD')

        if not email or not password:
            self.stdout.write(self.style.ERROR('Email and password must be set via --email or environ.'))
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f"User with email {email} already exists."))
        else:
            try:
                user = User.objects.create(
                    email=email,
                    first_name='Admin',
                    last_name='Admin1',
                    is_staff=True,
                    is_superuser=True
                )

                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Superuser {email} created successfully."))
            except IntegrityError as e:
                self.stdout.write(self.style.ERROR(f"Failed to create superuser: {str(e)}"))