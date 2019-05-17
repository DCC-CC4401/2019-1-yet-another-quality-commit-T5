from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.edit import UpdateView

from .models import Evaluador
from .forms import AddEvaluador


def post_evaluadores(request):
    form = AddEvaluador()
    return render(request, 'evaluadores/evaluadores_admin.html', {'form': form})


def add_evaluador(request):
    if request.POST:
        form = AddEvaluador(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('evaluadores')
        else:
            form = AddEvaluador()

    return render(request, 'evaluadores/evaluadores_admin.html', {'form': form})


def all_evaluadores(request):
    evaluadores = Evaluador.objects.all()
    evaluadores_list = []

    for evaluador in evaluadores:
        evaluadores_list.append(evaluador)

    form = AddEvaluador()

    return render(request, 'evaluadores/evaluadores_admin.html', {'evaluadores': evaluadores_list, 'form':form})