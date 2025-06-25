# Seu_projeto_django/urls.py
from django.contrib import admin
from django.urls import path, include
from TodayHabits.views import Login, Logout, AutenticacaoAPIView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('habito/', include('habito.urls')),
    # path('habito/', include('habito.urls')), # Se usar esta, a URL no Angular seria 'http://127.0.0.1:8000/habito/habitos/'
    path('api/', include('habito.urls')), 
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('autenticacao-api/', AutenticacaoAPIView.as_view(), name='autenticacao-api'),
]