from django.shortcuts import render

from rest_framework import viewsets, filters
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

    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'telefono']


class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'cliente__nombre',
        'cliente__telefono',
    ]

    def get_queryset(self):
        queryset = super().get_queryset()

        fecha = self.request.query_params.get('fecha')
        estado = self.request.query_params.get('estado')

        if fecha:
            queryset = queryset.filter(fecha=fecha)

        if estado:
            queryset = queryset.filter(estado=estado)

        return queryset


class VoucherViewSet(viewsets.ModelViewSet):
    queryset = Voucher.objects.all()
    serializer_class = VoucherSerializer


class RepresentanteViewSet(viewsets.ModelViewSet):
    queryset = Representante.objects.all()
    serializer_class = RepresentanteSerializer