from django.shortcuts import render, redirect
from .models import Habito, CheckDiario
from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required
def lista_habitos(request):
    habitos = Habito.objects.filter(user=request.user)  # Filtra hábitos do usuário autenticado
    today_checks = CheckDiario.objects.filter(data=timezone.now().date(), habito__user=request.user)

    checks_dict = {check.habito.id: check for check in today_checks}

    habitos_com_checks = []
    for habito in habitos:
        check_status = checks_dict.get(habito.id)
        habitos_com_checks.append({
            'habito': habito,
            'check': check_status
        })

    context = {
        'habitos_com_checks': habitos_com_checks,
    }

    return render(request, 'habito/lista_habitos.html', context)

@login_required
def marcar_habito(request, id):
    habito = Habito.objects.get(id=id, user=request.user)  # Certifica-se de que o hábito pertence ao usuário
    check, created = CheckDiario.objects.get_or_create(habito=habito, data=timezone.now().date())
    check.feito = not check.feito
    check.save()
    return redirect('lista_habitos')

@login_required
def novo_habito(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        Habito.objects.create(nome=nome, descricao=descricao, user=request.user)  # Associa ao usuário autenticado
        return redirect('lista_habitos')
    return render(request, 'habito/novo_habito.html')

@login_required
def editar_habito(request, id):
    habito = Habito.objects.get(id=id, user=request.user)  # Certifica-se de que o hábito pertence ao usuário
    if request.method == 'POST':
        habito.nome = request.POST.get('nome')
        habito.descricao = request.POST.get('descricao')
        habito.save()
        return redirect('lista_habitos')
    return render(request, 'habito/editar_habito.html', {'habito': habito})

@login_required
def excluir_habito(request, id):
    habito = Habito.objects.get(id=id, user=request.user)  # Certifica-se de que o hábito pertence ao usuário
    habito.delete()
    return redirect('lista_habitos')

@login_required
def calendario(request):
    hoje = timezone.now().date()
    dias = CheckDiario.objects.filter(habito__user=request.user).values_list('data', flat=True).distinct()

    dias_completos = []
    for dia in dias:
        checks_no_dia = CheckDiario.objects.filter(data=dia, habito__user=request.user)
        if checks_no_dia.count() == Habito.objects.filter(user=request.user).count() and all(check.feito for check in checks_no_dia):
            dias_completos.append(dia)

    context = {
        'hoje': hoje,
        'dias': dias,
        'dias_completos': dias_completos,
    }
    return render(request, 'habito/calendario.html', context)