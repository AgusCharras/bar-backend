from django.contrib import admin

# Register your models here.

from .models import Cliente, Reserva, Voucher, Representante

admin.site.register(Cliente)
admin.site.register(Reserva)
admin.site.register(Voucher)
admin.site.register(Representante)