from django.views.generic import View
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.conf import settings

class Login(View):
	

    def get(self, request):
        contexto = {'mensagem': ''}
        if request.user.is_authenticated:
            return redirect("/veiculo")
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
                return redirect("/veiculo")
            
            return render(request, 'autenticacao.html', {'mensagem' : 'Usuário inativo'})
        return render(request, 'autenticacao.html',{'mensagem' : 'Usuário ou senha inválidos'})

class Logout(View):

    def get(seel, request):
        logout(request)
        return redirect(settings.LOGIN_URL)