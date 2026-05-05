from django.db import models

# =========================
# ENUMS / CHOICES
# =========================

class EstadoContacto(models.TextChoices):
    RESERVO = "reservo", "Reservó"
    NO_RESERVO = "no_reservo", "No reservó"
    NO_CONTESTO = "no_contesto", "No contestó"


class Turno(models.TextChoices):
    TARDE = "tarde", "Tarde"
    NOCHE = "noche", "Noche"
    AMBOS = "ambos", "Tarde/Noche"


class EstadoVoucher(models.TextChoices):
    ACTIVO = "activo", "Activo"
    INACTIVO = "inactivo", "Inactivo"


class EstadoRepresentante(models.TextChoices):
    ACTIVO = "activo", "Activo"
    INACTIVO = "inactivo", "Inactivo"


class EstadoReserva(models.TextChoices):
    A_CONFIRMAR = "a_confirmar", "Falta confirmar"
    RESERVADO = "reservado", "Reservado"
    CANCELADO = "cancelado", "Cancelado"
    COMPLETADO = "completado", "Completado"
    NO_SHOW = "no_show", "No asistió"


# =========================
# MODELOS
# =========================

class Cliente(models.Model):
    nombre = models.CharField(max_length=150)
    telefono = models.CharField(max_length=20, unique=True)
    cumpleanios = models.DateField(null=True, blank=True)

    estado_contacto = models.CharField(
        max_length=20,
        choices=EstadoContacto.choices,
        default=EstadoContacto.NO_CONTESTO
    )

    turno = models.CharField(
        max_length=10,
        choices=Turno.choices,
        default=Turno.AMBOS
    )

    aprobado = models.BooleanField(default=True)

    observaciones = models.TextField(blank=True)

    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Voucher(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    estado = models.CharField(
        max_length=10,
        choices=EstadoVoucher.choices,
        default=EstadoVoucher.ACTIVO
    )

    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Representante(models.Model):
    nombre = models.CharField(max_length=150)
    apodo = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=20, unique=True)

    estado = models.CharField(
        max_length=10,
        choices=EstadoRepresentante.choices,
        default=EstadoRepresentante.ACTIVO
    )

    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.apodo or self.nombre


class Reserva(models.Model):
    
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="reservas"
    )

    representante = models.ForeignKey(
        Representante,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reservas"
    )

    vouchers = models.ManyToManyField(
        Voucher,
        blank=True,
        related_name="reservas"
    )

    fecha = models.DateField()
    hora_inicio = models.TimeField()
    #hora_fin = models.TimeField(null=True, blank=True)

    cantidad_personas = models.PositiveIntegerField()
    
    cantidad_personas_reales = models.PositiveIntegerField(
        null=True,
        blank=True
    )    

    estado = models.CharField(
        max_length=15,
        choices=EstadoReserva.choices,
        default=EstadoReserva.RESERVADO
    )

    observaciones = models.TextField(blank=True)

    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cliente.nombre} - {self.fecha} {self.hora_inicio}"
    
    class Meta:
        ordering = ['-fecha', '-hora_inicio']