from rest_framework import serializers
from .models import Cliente, Reserva, Voucher, Representante, Entrada, AsistenciaRepresentante, Embajador, AsistenciaEmbajador

'''
Estos Serializers convierten:
MODELOS -> JSON
JSON -> MODELOS
'''



class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'


class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = '__all__'


class RepresentanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Representante
        fields = '__all__'

class EmbajadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Embajador
        fields = '__all__'
        
class ReservaSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)

    class Meta:
        model = Reserva
        fields = '__all__'
        
    def validate_hora_inicio(self, value):
        if value.minute not in [0, 30]:
            raise serializers.ValidationError(
                "La hora debe ser en intervalos de 30 minutos."
            )
        return value
    
class EntradaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrada
        fields = '__all__'


class AsistenciaRepresentanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsistenciaRepresentante
        fields = '__all__'
        
class AsistenciaEmbajadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsistenciaEmbajador
        fields = '__all__'