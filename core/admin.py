from django.contrib import admin

# Register your models here.

from .models import Cliente, Reserva, Voucher, Representante, Entrada, AsistenciaRepresentante

admin.site.register(Cliente)
admin.site.register(Reserva)
admin.site.register(Voucher)
admin.site.register(Representante)
admin.site.register(Entrada)
admin.site.register(AsistenciaRepresentante)