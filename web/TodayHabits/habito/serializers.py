from datetime import date
from rest_framework import serializers
from .models import Habito, CheckDiario

class HabitoSerializer(serializers.ModelSerializer):
    ultima_data_feito = serializers.SerializerMethodField()
    feito = serializers.SerializerMethodField()  # ✅ Campo novo

    class Meta:
        model = Habito
        fields = ['id', 'nome', 'descricao', 'user', 'ultima_data_feito', 'feito']
        read_only_fields = ['id', 'user', 'ultima_data_feito', 'feito']

    def get_ultima_data_feito(self, obj):
        ultimo_check = obj.checks.filter(feito=True).order_by('-data').first()
        if ultimo_check:
            return ultimo_check.data
        return None

    def get_feito(self, obj):
        check = obj.checks.filter(data=date.today()).first()
        return check.feito if check else False

class CheckDiarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckDiario
        fields = ['id', 'habito', 'data', 'feito']
