# habito/urls.py
from django.urls import path
from . import views
from .api_views import (
    APIListarHabitos, APICriarHabito, APIEditarHabito, APIDeletarHabito,
    APIMarcarHabito, APICalendario
)

urlpatterns = [
    path('', views.lista_habitos, name='lista_habitos'),
    path('<int:id>/marcar/', views.marcar_habito, name='marcar_habito'),
    path('novo/', views.novo_habito, name='novo_habito'),
    path('<int:id>/editar/', views.editar_habito, name='editar_habito'),
    path('<int:id>/excluir/', views.excluir_habito, name='excluir_habito'),
    path('calendario/', views.calendario, name='calendario'),

    # Remova 'api/' daqui, já que o urls.py principal já adiciona 'api/'
    path('habitos/', APIListarHabitos.as_view(), name='api_listar_habitos'),
    path('habitos/criar/', APICriarHabito.as_view(), name='api_criar_habito'),
    path('habitos/<int:pk>/editar/', APIEditarHabito.as_view(), name='api_editar_habito'),
    path('habitos/<int:pk>/deletar/', APIDeletarHabito.as_view(), name='api_deletar_habito'),
    path('habitos/<int:pk>/marcar/', APIMarcarHabito.as_view(), name='api_marcar_habito'),
    path('calendario/', APICalendario.as_view(), name='api_calendario'), # Se esta for a API do calendário
]