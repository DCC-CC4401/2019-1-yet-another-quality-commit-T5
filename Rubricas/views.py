from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from Rubricas.forms import *


@login_required
def post_rubricas(request):
    """
    Vista principal de rubricas, que contiene todas las rubricas existentes en la plataforma.
    :param request:
    :return:
    """
    form = AddRubrica()
    rubricas = AspectoRubrica.objects.all()
    rubrica_list = []

    for rubrica in rubricas:
        rubrica_list.append(rubrica)

    # form = AddEvaluador()
    # print(evaluadores_list)
    return render(request, 'rubrica/rubrica_admin.html', {'form': form, 'rubrica_list': rubrica_list})


@login_required()
def add_rubrica(request):
    """
    Agrega una rubrica, en caso de la request involucre a un Profesor.
    :param request:
    :return:
    """
    if request.POST and request.user.groups.filter(name='Profesores').exists():
        form = AddRubrica(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('rubrica')
        else:
            form = AddRubrica()
            return render(request, 'rubrica/rubrica_admin.html', {'form': form})
    return post_rubricas(request)


@login_required()
def all_rubrica(request):
    """
    Devuelve todas las rubricas existentes en la plataforma.
    :param request:
    :return:
    """
    rubricas = AspectoRubrica.objects.all()
    rubrica_list = []

    for rubrica in rubricas:
        rubrica_list.append(rubrica)

    form = AddRubrica()

    return render(request, 'rubrica/rubrica_admin.html', {'rubrica': rubrica_list, 'form':form})
