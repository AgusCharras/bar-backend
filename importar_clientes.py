import os
import django
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from core.models import Cliente
from django.db import connection

# Leer CSV
df = pd.read_csv("clientes_limpios.csv")

# Obtener teléfonos existentes UNA sola vez
telefonos_existentes = set(
    Cliente.objects.values_list("telefono", flat=True)
)

clientes_nuevos = []

for _, row in df.iterrows():

    telefono = str(row["telefono"]).strip()

    # evitar duplicados
    if telefono in telefonos_existentes:
        continue

    cliente = Cliente(
        nombre=row["nombre"],
        telefono=telefono,
        cumpleanios=row["cumpleanios"] if pd.notna(row["cumpleanios"]) else None,
        estado_contacto=row["estado_contacto"],
        turno=row["turno"],
        aprobado=str(row["aprobado"]).lower() == "true",
        observaciones=row["observaciones"]
        if pd.notna(row["observaciones"])
        else "",
    )

    clientes_nuevos.append(cliente)

# insertar en bloques
BATCH_SIZE = 500

for i in range(0, len(clientes_nuevos), BATCH_SIZE):

    lote = clientes_nuevos[i:i + BATCH_SIZE]

    Cliente.objects.bulk_create(lote)

    # cerrar conexión para evitar timeout
    connection.close()

    print(f"Lote {i} insertado")

print("Importación finalizada")