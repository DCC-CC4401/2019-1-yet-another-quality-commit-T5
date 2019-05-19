from django.shortcuts import render
from django.http import HttpResponseRedirect
from Rubricas.forms import *

def post_rubricas(request):
    form = AddRubrica()
    rubricas = AspectoRubrica.objects.all()
    rubrica_list = []

    for rubrica in rubricas:
        rubrica_list.append(rubrica)

    # form = AddEvaluador()
    # print(evaluadores_list)
    return render(request, 'rubrica/rubrica_admin.html', {'form': form, 'rubrica_list': rubrica_list})

def add_rubrica(request):
    if request.POST:
        form = AddRubrica(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('rubrica')
        else:
            form = AddRubrica()

        return render(request, 'rubrica/rubrica_admin.html', {'form': form})

def all_rubrica(request):
    rubricas = AspectoRubrica.objects.all()
    rubrica_list = []

    for rubrica in rubricas:
        rubrica_list.append(rubrica)

    form = AddRubrica()

    return render(request, 'rubrica/rubrica_admin.html', {'rubrica': rubrica_list, 'form':form})

