import csv
from django.core.management.base import BaseCommand
from core.models import Cliente

class Command(BaseCommand):
    help = 'Importar clientes desde CSV'

    def handle(self, *args, **kwargs):
        with open('clientes_limpios.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            total = 0
            creados = 0
            ignorados = 0

            for row in reader:
                total += 1

                telefono = row['telefono']

                if not telefono:
                    ignorados += 1
                    continue

                # evitar duplicados
                if Cliente.objects.filter(telefono=telefono).exists():
                    ignorados += 1
                    continue

                Cliente.objects.create(
                    nombre=row['nombre'][:150],
                    telefono=telefono,
                    cumpleanios=row['cumpleanios'] or None,
                    estado_contacto=row['estado_contacto'],
                    turno=row['turno'],
                    aprobado=row['aprobado'] == 'True',
                    observaciones=row['observaciones']
                )

                creados += 1

                if total % 1000 == 0:
                    self.stdout.write(f"Procesados: {total}")

        self.stdout.write(self.style.SUCCESS(
            f"✔ Total: {total} | Creados: {creados} | Ignorados: {ignorados}"
        ))