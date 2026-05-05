from django.shortcuts import render

from rest_framework import viewsets, filters
from .models import Cliente, Reserva, Voucher, Representante
from .serializers import (
    ClienteSerializer,
    ReservaSerializer,
    VoucherSerializer,
    RepresentanteSerializer
)

from rest_framework.permissions import IsAuthenticated
from .permissions import EsRepresentante, EsEncargadoOJefe, EsJefe, PuedeCrearCliente

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
    
    def get_permissions(self):
        if self.action == 'create':
            #return [IsAuthenticated(), (PuedeCrearCliente())]
            return []
        #return [IsAuthenticated()]
        return []


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

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            #return [IsAuthenticated(), (EsEncargadoOJefe())]
            return []
        #return [IsAuthenticated()]
        return []

class VoucherViewSet(viewsets.ModelViewSet):
    queryset = Voucher.objects.all()
    serializer_class = VoucherSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated(), EsJefe()]
        #return [IsAuthenticated()]
        return []
        


class RepresentanteViewSet(viewsets.ModelViewSet):
    queryset = Representante.objects.all()
    serializer_class = RepresentanteSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated(), EsJefe()]
        #return [IsAuthenticated()]
        return []