from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Crea un superusuario por defecto si no existe"

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@agrosur.pe", "admin123")
            self.stdout.write(self.style.SUCCESS("Superusuario creado: admin / admin123"))
        else:
            self.stdout.write("El usuario admin ya existe.")
