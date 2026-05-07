from rest_framework import serializers
from .models import Cliente, Reserva, Voucher, Representante

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