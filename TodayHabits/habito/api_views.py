from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import HabitoSerializer, CheckDiarioSerializer
from .models import Habito, CheckDiario
from django.utils import timezone

class APIListarHabitos(ListAPIView):
    serializer_class = HabitoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habito.objects.all()

class APICriarHabito(CreateAPIView):
    serializer_class = HabitoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class APIEditarHabito(RetrieveUpdateAPIView):
    serializer_class = HabitoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habito.objects.all()

class APIDeletarHabito(DestroyAPIView):
    serializer_class = HabitoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        pk = self.kwargs.get('pk')
        return Habito.objects.get(pk=pk)

class APIMarcarHabito(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        habito = Habito.objects.get(pk=pk)
        check, created = CheckDiario.objects.get_or_create(habito=habito, data=timezone.now().date())
        check.feito = not check.feito
        check.save()
        return Response({'status': 'success', 'feito': check.feito})

class APICalendario(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        hoje = timezone.now().date()
        dias = CheckDiario.objects.values_list('data', flat=True).distinct()

        dias_completos = []
        for dia in dias:
            checks_no_dia = CheckDiario.objects.filter(data=dia)
            if checks_no_dia.count() == Habito.objects.count() and all(check.feito for check in checks_no_dia):
                dias_completos.append(dia)

        return Response({'hoje': hoje, 'dias_completos': dias_completos})