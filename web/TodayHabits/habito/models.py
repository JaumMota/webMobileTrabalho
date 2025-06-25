from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Habito(models.Model):
    nome = models.CharField(max_length=100) # Nome do hábito
    descricao = models.TextField() # Descrição do hábito
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona o hábito ao usuário
    data = models.DateField(auto_now_add=True) # Data de criação do hábito

    def __str__(self):
        return self.nome

class CheckDiario(models.Model):
    habito = models.ForeignKey(Habito, on_delete=models.CASCADE, related_name='checks')
    data = models.DateField(default=timezone.now)
    feito = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.habito.nome} - {self.data} - {'Feito' if self.feito else 'Não feito'}"
