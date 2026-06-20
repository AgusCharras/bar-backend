from django.shortcuts import render

from rest_framework import viewsets, filters
from .models import Cliente, Reserva, Voucher, Representante, Entrada, AsistenciaRepresentante, Embajador, AsistenciaEmbajador
from .serializers import (
    ClienteSerializer,
    ReservaSerializer,
    VoucherSerializer,
    RepresentanteSerializer,
    EntradaSerializer,
    AsistenciaRepresentanteSerializer,
    EmbajadorSerializer,
    AsistenciaEmbajadorSerializer
)

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .permissions import EsRepresentante, EsEncargadoOJefe, EsJefe, PuedeCrearCliente
from django.db.models import Q, Sum, Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action



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
        
        #queryset = queryset.exclude(cumpleanios__isnull=True)
        
        dia = self.request.query_params.get("dia")
        mes = self.request.query_params.get("mes")
        
        if dia or mes:
            queryset = queryset.exclude(cumpleanios__isnull=True)
        
        if dia:
            queryset = queryset.filter(cumpleanios__day=dia)
            
        if mes:
            queryset = queryset.filter(cumpleanios__month=mes)
        
        return queryset
    
    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), (PuedeCrearCliente())]
            #return []
        return [IsAuthenticated()]
        #return []


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
            return [IsAuthenticated(), (EsEncargadoOJefe())]
            #return []
        return [IsAuthenticated()]
        #return []

class VoucherViewSet(viewsets.ModelViewSet):
    queryset = Voucher.objects.all()
    serializer_class = VoucherSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated(), EsJefe()]
        return [IsAuthenticated()]
        #return []
        


class RepresentanteViewSet(viewsets.ModelViewSet):
    queryset = Representante.objects.all()
    serializer_class = RepresentanteSerializer
    
    pagination_class = None

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated(), EsJefe()]
        return [IsAuthenticated()]
        #return []
        
class EmbajadorViewSet(viewsets.ModelViewSet):
    queryset = Embajador.objects.all()
    serializer_class = EmbajadorSerializer
    
    pagination_class = None

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated(), (EsEncargadoOJefe())]
        
        return [IsAuthenticated()]
    
class EntradaViewSet(viewsets.ModelViewSet):

    queryset = Entrada.objects.select_related(
        'representante'
    )

    serializer_class = EntradaSerializer

    filter_backends = [filters.SearchFilter]

    search_fields = [
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
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated(), (EsEncargadoOJefe())]
        return [IsAuthenticated()]
        #return []
    
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
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated(), (EsEncargadoOJefe())]
        return [IsAuthenticated()]
        #return []
        
class AsistenciaEmbajadorViewSet(viewsets.ModelViewSet):

    queryset = AsistenciaEmbajador.objects.select_related(
        'embajador'
    )

    serializer_class = AsistenciaEmbajadorSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        fecha = self.request.query_params.get('fecha')

        if fecha:
            queryset = queryset.filter(fecha=fecha)

        return queryset
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated(), (EsEncargadoOJefe())]
        return [IsAuthenticated()]
        #return []
        
class ReportesViewSet(viewsets.ViewSet):

    #permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def reservas(self, request):

        fecha = request.query_params.get('fecha')
        desde = request.query_params.get('desde')
        hasta = request.query_params.get('hasta')

        reservas = Reserva.objects.select_related(
            'representante'
        )

        if fecha:
            reservas = reservas.filter(fecha=fecha)

        if desde:
            reservas = reservas.filter(fecha__gte=desde)

        if hasta:
            reservas = reservas.filter(fecha__lte=hasta)

        resumen = reservas.aggregate(
            cantidad_reservas=Count('id'),
            esperados=Sum('cantidad_personas'),
            reales=Sum('cantidad_personas_reales')
        )

        esperados = resumen['esperados'] or 0
        reales = resumen['reales'] or 0
        faltaron = esperados - reales

        porcentaje_asistencia = 0

        if esperados > 0:
            porcentaje_asistencia = round(
                (reales / esperados) * 100,
                2
            )

        representantes = (
            reservas
            .exclude(representante__isnull=True)
            .values(
                'representante__id',
                'representante__nombre',
                'representante__apodo'
            )
            .annotate(
                cantidad_reservas=Count('id'),
                esperados=Sum('cantidad_personas'),
                reales=Sum('cantidad_personas_reales')
            )
            .order_by('-reales')
        )

        representantes_limpios = []

        for rep in representantes:

            esperados_rep = rep['esperados'] or 0
            reales_rep = rep['reales'] or 0

            faltaron_rep = esperados_rep - reales_rep

            porcentaje_rep = 0

            if esperados_rep > 0:
                porcentaje_rep = round(
                    (reales_rep / esperados_rep) * 100,
                    2
                )

            representantes_limpios.append({
                "id": rep["representante__id"],
                "nombre": rep["representante__nombre"],
                "apodo": rep["representante__apodo"],
                "cantidad_reservas": rep["cantidad_reservas"],
                "esperados": esperados_rep,
                "reales": reales_rep,
                "faltaron": faltaron_rep,
                "porcentaje_asistencia": porcentaje_rep
            })

        representantes_limpios.sort(
            key=lambda x: x["reales"],
            reverse=True
        )

        return Response({
            "resumen": {
                "cantidad_reservas": resumen['cantidad_reservas'] or 0,
                "esperados": esperados,
                "reales": reales,
                "faltaron": faltaron,
                "porcentaje_asistencia": porcentaje_asistencia
            },
            "representantes": representantes_limpios
        })