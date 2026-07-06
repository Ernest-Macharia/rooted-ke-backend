from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create or update a superuser from environment variables."

    def handle(self, *args, **options):
        User = get_user_model()

        username = self._get_required_env("DJANGO_SUPERUSER_USERNAME")
        email = self._get_required_env("DJANGO_SUPERUSER_EMAIL")
        password = self._get_required_env("DJANGO_SUPERUSER_PASSWORD")
        first_name = self._get_optional_env("DJANGO_SUPERUSER_FIRST_NAME")
        last_name = self._get_optional_env("DJANGO_SUPERUSER_LAST_NAME")

        user, created = User.objects.get_or_create(username=username, defaults={"email": email})

        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True

        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name

        user.set_password(password)
        user.save()

        action = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"{action} superuser '{username}'."))

    def _get_required_env(self, name):
        from os import getenv

        value = getenv(name, "").strip()
        if not value:
            raise CommandError(f"{name} is required.")
        return value

    def _get_optional_env(self, name):
        from os import getenv

        return getenv(name, "").strip()
