from django.views.generic import View
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

class Login(View):
	

    def get(self, request):
        contexto = {'mensagem': ''}
        if request.user.is_authenticated:
            return redirect("/habito")
        else:
            return render(request, 'autenticacao.html', contexto)

    def post(self, request):

        # Obtém as credenciais de autenticação do formulário
        usuario = request.POST.get('usuario', None)
        senha = request.POST.get('senha', None)


        user = authenticate(request, username=usuario, password=senha)
        if user is not None:

            #Verifica se o usuário ainda está ativo no sistema
            if user.is_active:
                login(request, user)
                return redirect("/habito")
            
            return render(request, 'autenticacao.html', {'mensagem' : 'Usuário inativo'})
        return render(request, 'autenticacao.html',{'mensagem' : 'Usuário ou senha inválidos'})

class Logout(View):

    def get(seel, request):
        logout(request)
        return redirect(settings.LOGIN_URL)
    
class LoginAPI(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={
                'request': request
            }
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'id': user.id,
            'nome': user.first_name,
            'email': user.email,
            'token': token.key
        })

class AutenticacaoAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Autentica o usuário
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                # Gera ou recupera o token de autenticação
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    "id": user.id,
                    "nome": user.first_name,
                    "email": user.email,
                    "token": token.key
                }, status=HTTP_200_OK)
            return Response({"error": "Usuário inativo"}, status=HTTP_400_BAD_REQUEST)
        return Response({"error": "Credenciais inválidas"}, status=HTTP_400_BAD_REQUEST)
