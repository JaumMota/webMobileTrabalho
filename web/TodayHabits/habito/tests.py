from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Habito, CheckDiario

# Classe de testes para as views relacionadas a hábitos
class HabitoViewTests(TestCase):
    # Método chamado antes de cada teste para preparar os dados
    def setUp(self):
        self.client = Client()  # Cliente para simular requisições HTTP
        # Criação e login de um usuário de teste
        self.user = User.objects.create_user(username='teste', password='senha123')
        self.client.login(username='teste', password='senha123')

        # Cria um hábito associado ao usuário
        self.habito = Habito.objects.create(nome='Beber água', descricao='Beber 2L de água', user=self.user)
        # Outro usuário (não utilizado diretamente aqui, mas útil para testes futuros)
        self.outro_usuario = User.objects.create_user(username='outro', password='senha456')
        # URL da view de lista de hábitos
        self.url_lista = reverse('lista_habitos')

    # Testa a visualização da lista de hábitos
    def test_lista_habitos_view(self):
        response = self.client.get(self.url_lista)
        self.assertEqual(response.status_code, 200)  # Verifica se a página carregou com sucesso
        self.assertTemplateUsed(response, 'habito/lista_habitos.html')  # Confirma o template utilizado
        self.assertIn('habitos_com_checks', response.context)  # Verifica se a variável de contexto está presente

    # Testa a marcação e desmarcação (toggle) do hábito no mesmo dia
    def test_marcar_habito_toggle(self):
        url = reverse('marcar_habito', args=[self.habito.id])
        self.client.get(url)  # Primeira marcação (deve criar e marcar como feito)
        check = CheckDiario.objects.get(habito=self.habito, data=timezone.now().date())
        self.assertTrue(check.feito)  # Confirma que foi marcado como feito

        # Segunda chamada (toggle), deve desmarcar
        self.client.get(url)
        check.refresh_from_db()
        self.assertFalse(check.feito)  # Verifica que foi desmarcado

    # Testa o envio de formulário para criação de um novo hábito (POST)
    def test_novo_habito_post(self):
        url = reverse('novo_habito')
        data = {'nome': 'Novo Hábito', 'descricao': 'Descrição'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Deve redirecionar após criação
        self.assertTrue(Habito.objects.filter(nome='Novo Hábito').exists())  # Verifica se o hábito foi criado

    # Testa o acesso à página de novo hábito (GET)
    def test_novo_habito_get(self):
        url = reverse('novo_habito')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'habito/novo_habito.html')  # Confirma que o template correto foi renderizado

    # Testa o envio do formulário de edição de um hábito
    def test_editar_habito_post(self):
        url = reverse('editar_habito', args=[self.habito.id])
        response = self.client.post(url, {'nome': 'Atualizado', 'descricao': 'Nova desc'})
        self.habito.refresh_from_db()
        self.assertEqual(self.habito.nome, 'Atualizado')  # Verifica se o nome foi atualizado
        self.assertEqual(response.status_code, 302)  # Espera redirecionamento

    # Testa o acesso à página de edição (GET)
    def test_editar_habito_get(self):
        url = reverse('editar_habito', args=[self.habito.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'habito/editar_habito.html')  # Verifica o template renderizado

    # Testa a exclusão de um hábito
    def test_excluir_habito(self):
        url = reverse('excluir_habito', args=[self.habito.id])
        response = self.client.get(url)
        self.assertFalse(Habito.objects.filter(id=self.habito.id).exists())  # Verifica se foi removido do banco
        self.assertEqual(response.status_code, 302)  # Espera redirecionamento

    # Testa a visualização do calendário de hábitos
    def test_calendario_view(self):
        # Cria um check de hábito feito no dia atual
        CheckDiario.objects.create(habito=self.habito, data=timezone.now().date(), feito=True)
        url = reverse('calendario')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'habito/calendario.html')
        self.assertIn('dias_completos', response.context)  # Verifica se a lista de dias completos está no contexto
