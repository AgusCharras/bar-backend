from django.shortcuts import render

from rest_framework import viewsets, filters
from .models import Cliente, Reserva, Voucher, Representante, Entrada, AsistenciaRepresentante
from .serializers import (
    ClienteSerializer,
    ReservaSerializer,
    VoucherSerializer,
    RepresentanteSerializer,
    EntradaSerializer,
    AsistenciaRepresentanteSerializer
)

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .permissions import EsRepresentante, EsEncargadoOJefe, EsJefe, PuedeCrearCliente
from django.db.models import Q


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

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['nombre', 'telefono']
    filterset_fields = ['turno']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        queryset = queryset.exclude(cumpleanios__isnull=True)
        
        dia = self.request.query_params.get("dia")
        mes = self.request.query_params.get("mes")
        
        if dia:
            queryset = queryset.filter(cumpleanios__day=dia)
            
        if mes:
            queryset = queryset.filter(cumpleanios__month=mes)
        
        return queryset
    
    def get_permissions(self):
        if self.action == 'create':
            #return [IsAuthenticated(), (PuedeCrearCliente())]
            return []
        #return [IsAuthenticated()]
        return []


class ReservaViewSet(viewsets.ModelViewSet):
    #queryset = Reserva.objects.all()

    queryset = Reserva.objects.select_related(
        'cliente',
        'representante'
    ).prefetch_related(
        'vouchers'
    )
    
    serializer_class = ReservaSerializer
    
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'cliente__nombre',
        'cliente__telefono',
    ]

    def get_queryset(self):
        queryset = super().get_queryset()

        fecha = self.request.query_params.get('fecha')
        fecha_desde = self.request.query_params.get('fecha_desde')
        fecha_hasta = self.request.query_params.get('fecha_hasta')
        estado = self.request.query_params.get('estado')
        representante = self.request.query_params.get('representante')
        turno = self.request.query_params.get('turno')
        hora = self.request.query_params.get('hora')

        if fecha:
            queryset = queryset.filter(fecha=fecha)
            
        if fecha_desde:
            queryset = queryset.filter(fecha__gte = fecha_desde)
            
        if fecha_hasta:
            queryset = queryset.filter(fecha__lte = fecha_hasta)

        if estado:
            queryset = queryset.filter(estado=estado)
            
        if representante:
            queryset = queryset.filter(Q(representante__nombre__icontains=representante) | Q(representante__apodo__icontains=representante))

        if turno:
            queryset = queryset.filter(cliente__turno=turno)
            
        if hora:
            queryset = queryset.filter(hora_inicio=hora)
            
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
    
class EntradaViewSet(viewsets.ModelViewSet):

    queryset = Entrada.objects.select_related(
        'representante'
    )

    serializer_class = EntradaSerializer

    filter_backends = [filters.SearchFilter]

    search_fields = [
        'cliente__nombre',
        'representante__nombre',
        'representante__apodo',
    ]

    def get_queryset(self):
        queryset = super().get_queryset()

        fecha = self.request.query_params.get('fecha')
        tipo = self.request.query_params.get('tipo')

        if fecha:
            queryset = queryset.filter(fecha=fecha)

        if tipo:
            queryset = queryset.filter(tipo=tipo)

        return queryset
    
class AsistenciaRepresentanteViewSet(viewsets.ModelViewSet):

    queryset = AsistenciaRepresentante.objects.select_related(
        'representante'
    )

    serializer_class = AsistenciaRepresentanteSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        fecha = self.request.query_params.get('fecha')

        if fecha:
            queryset = queryset.filter(fecha=fecha)

        return queryset