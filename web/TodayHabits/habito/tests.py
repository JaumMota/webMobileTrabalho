from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import Habito, CheckDiario

class TestesModelHabito(TestCase):
    def setUp(self):
        self.instancia = Habito.objects.create(nome="Exercício", descricao="Fazer exercícios diariamente")

    def test_str(self):
        self.assertEqual(str(self.instancia), "Exercício")

class TestesModelCheckDiario(TestCase):
    def setUp(self):
        self.habito = Habito.objects.create(nome="Exercício", descricao="Fazer exercícios diariamente")
        self.instancia = CheckDiario.objects.create(habito=self.habito, data=timezone.now().date(), feito=True)

    def test_str(self):
        self.assertEqual(str(self.instancia), f"{self.habito.nome} - {self.instancia.data} - Feito")

class TestesViewListaHabitos(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='teste123')
        self.client.force_login(self.user)
        self.url = reverse('lista_habitos')
        Habito.objects.create(nome="Exercício", descricao="Fazer exercícios diariamente")

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'habito/lista_habitos.html')
        self.assertEqual(len(response.context['habitos_com_checks']), 1)

class TestesViewCriarHabito(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='teste123')
        self.client.force_login(self.user)
        self.url = reverse('novo_habito')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'habito/novo_habito.html')

    def test_post(self):
        data = {'nome': 'Leitura', 'descricao': 'Ler um livro diariamente'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('lista_habitos'))
        self.assertEqual(Habito.objects.count(), 1)
        self.assertEqual(Habito.objects.first().nome, 'Leitura')

class TestesViewEditarHabito(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='teste123')
        self.client.force_login(self.user)
        self.instancia = Habito.objects.create(nome="Exercício", descricao="Fazer exercícios diariamente")
        self.url = reverse('editar_habito', kwargs={'id': self.instancia.id})

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'habito/editar_habito.html')
        self.assertEqual(response.context.get('habito').id, self.instancia.id)

    def test_post(self):
        data = {'nome': 'Exercício Editado', 'descricao': 'Descrição editada'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('lista_habitos'))
        self.instancia.refresh_from_db()
        self.assertEqual(self.instancia.nome, 'Exercício Editado')

class TestesViewExcluirHabito(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='teste123')
        self.client.force_login(self.user)
        self.instancia = Habito.objects.create(nome="Exercício", descricao="Fazer exercícios diariamente")
        self.url = reverse('excluir_habito', kwargs={'id': self.instancia.id})

    def test_post(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('lista_habitos'))
        self.assertEqual(Habito.objects.count(), 0)

class TestesViewMarcarHabito(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='teste123')
        self.client.force_login(self.user)
        self.instancia = Habito.objects.create(nome="Exercício", descricao="Fazer exercícios diariamente")
        self.url = reverse('marcar_habito', kwargs={'id': self.instancia.id})

    def test_post(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('lista_habitos'))
        check = CheckDiario.objects.get(habito=self.instancia, data=timezone.now().date())
        self.assertTrue(check.feito)

class TestesViewCalendario(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='teste123')
        self.client.force_login(self.user)
        self.url = reverse('calendario')
        Habito.objects.create(nome="Exercício", descricao="Fazer exercícios diariamente")

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'habito/calendario.html')