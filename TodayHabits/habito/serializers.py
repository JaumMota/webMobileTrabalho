from rest_framework import serializers
from .models import Habito, CheckDiario

class HabitoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habito
        fields = ['id', 'nome', 'descricao']

class CheckDiarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckDiario
        fields = ['id', 'habito', 'data', 'feito']