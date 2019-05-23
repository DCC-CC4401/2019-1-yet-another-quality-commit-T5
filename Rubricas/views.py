from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from Rubricas.forms import *

def post_rubricas(request):
    addForm = AddRubrica()
    rubricas = Rubrica.objects.all()
    rubricas_list = []

    for rubrica in rubricas:
        rubricas_list.append(rubrica)

    
    return render(request, 'rubrica/rubrica_admin.html', {'addForm': addForm, 'rubricas_list': rubricas_list})

def add_rubrica(request):
    if request.POST:
        #verificar si ya existe rubrica con ese nombre
        creadas = Rubrica.objects.filter(nombre__startswith=request.POST['nombre'])
        print(creadas.count())
        if creadas.count() > 0:
            ##caso en que existe mas de una rubrica con el mismo nombre
            messages.warning(request, 'El nombre ya está en uso')
            return HttpResponseRedirect('rubricas')
        
        form = AddRubrica(request.POST)
        if form.is_valid():
            form.save()
            ##caso exitoso
            messages.success(request, 'Rúbrica creada correctamente')
            return HttpResponseRedirect('rubricas')
        else:
            form = AddRubrica()

        return render(request, 'rubricas/rubrica_admin.html', {'addForm': form})

def all_rubrica(request):
    rubricas = AspectoRubrica.objects.all()
    rubrica_list = []

    for rubrica in rubricas:
        rubrica_list.append(rubrica)

    form = AddRubrica()

    return render(request, 'rubrica/rubrica_admin.html', {'rubrica': rubrica_list, 'form':form})

