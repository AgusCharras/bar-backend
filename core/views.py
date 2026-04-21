from django.shortcuts import render

from rest_framework import viewsets
from .models import Cliente, Reserva, Voucher, Representante
from .serializers import (
    ClienteSerializer,
    ReservaSerializer,
    VoucherSerializer,
    RepresentanteSerializer
)

'''
    ModelViewSet te da automaticamente:
        GET (listar)
        GET por id
        POST (crear)
        PUT/PATCH (editar)
        DELETE
'''


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer


class VoucherViewSet(viewsets.ModelViewSet):
    queryset = Voucher.objects.all()
    serializer_class = VoucherSerializer


class RepresentanteViewSet(viewsets.ModelViewSet):
    queryset = Representante.objects.all()
    serializer_class = RepresentanteSerializer