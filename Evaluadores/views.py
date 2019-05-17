from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.edit import UpdateView

from .forms import AddEvaluador


def post_evaluadores(request):
    form = AddEvaluador
    return render(request, 'evaluadores/evaluadores_admin.html', {'form': form})


def add_evaluador(request):
    if request.POST:
        form = AddEvaluador(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('evaluadores')
        else:
            form = AddEvaluador

    return render(request, 'evaluadores/evaluadores_admin.html', {'form': form})
