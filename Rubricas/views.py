from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from Rubricas.forms import *
from django.core import serializers
from django.http import HttpResponse

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
        creadas.order_by('fila','columna')
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

import json
def busqueda_rubrica_ajax(request):
    if request.GET:
        id_rubrica= request.GET['id']
        aspectos = AspectoRubrica.objects.filter(rubrica__id=id_rubrica)
        aspectos = aspectos.order_by('fila','columna')
        data = [ rubrica_serializer(aspecto)  for aspecto in aspectos] 
        return HttpResponse(json.dumps(data), content_type='application/json')
    
def rubrica_serializer(aspectoRubrica):
    return {'fila': aspectoRubrica.fila, 'columna' : aspectoRubrica.columna,
                'puntaje': str(aspectoRubrica.puntaje), 'nombreFila':aspectoRubrica.nombreFila,
                    'descripcion': aspectoRubrica.descripcion}