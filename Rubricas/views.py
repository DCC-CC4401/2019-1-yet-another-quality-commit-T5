from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from Rubricas.forms import *
from django.core import serializers
from django.http import HttpResponse
from Rubricas.models import *


@login_required
def post_rubricas(request):
    """
    Vista principal de rubricas, que contiene todas las rubricas existentes en la plataforma.
    :param request:
    :return:
    """
    addForm = AddRubrica()
    rubricas = Rubrica.objects.all()
    rubricas_list = []

    for rubrica in rubricas:
        rubricas_list.append(rubrica)

    
    return render(request, 'rubrica/rubrica_admin.html', {'addForm': addForm, 'rubricas_list': rubricas_list})


@login_required()
def add_rubrica(request):
        
    """
    Agrega una rubrica, en caso de la request involucre a un Profesor.
    :param request:
    :return:
    """
    if request.POST and request.user.groups.filter(name='Profesores').exists():
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
            return render(request, 'rubrica/rubrica_admin.html', {'form': form})
    return post_rubricas(request)


@login_required()
def all_rubrica(request):
    """
    Devuelve todas las rubricas existentes en la plataforma.
    :param request:
    :return:
    """
    rubricas = Rubrica.objects.all()
    rubrica_list = []

    for rubrica in rubricas:
        rubrica_list.append(rubrica)

    form = AddRubrica()

    return render(request, 'rubrica/rubrica_admin.html', {'rubrica': rubrica_list, 'form':form})

@login_required
def delete_rubrica(request):
    if request.POST and request.user.groups.filter(name='Profesores').exists():
        id = int(request.POST.get('id'))
        deleted = Rubrica.objects.get(pk=id).delete()
        if deleted is not None:
            ##caso exitoso
            messages.success(request, 'Rúbrica eliminada de la faz de la Tierra')
            return HttpResponseRedirect('rubricas')
    
    ##caso de error
    messages.warning(request, 'Error del servidor: no se pudo eliminar la rúbrica')        
    return post_rubricas(request)

import json
def busqueda_rubrica_ajax(request):
    if request.GET:
        id_rubrica= request.GET['id']
        aspectos = AspectoRubrica.objects.filter(rubrica__id=id_rubrica)
        aspectos = aspectos.order_by('fila','columna')
        grouped = []
        ##ahora agrupamos por fila, la salida es [[aspectosfila1][aspectosfila2][...]]
        for aspecto in aspectos:
            if (len(grouped)-1 < aspecto.fila):
                grouped.append([])
            grouped[aspecto.fila].append(aspectoRubrica_serializer(aspecto))
            
        return HttpResponse(json.dumps(grouped), content_type='application/json')
    

def aspectoRubrica_serializer(aspectoRubrica):
    return {'fila': aspectoRubrica.fila, 'columna' : aspectoRubrica.columna,
                'puntaje': str(aspectoRubrica.puntaje), 'nombreFila':aspectoRubrica.nombreFila,
                    'descripcion': aspectoRubrica.descripcion}


@login_required
def updateAspectosRubrica(request):
    if request.method == "POST":
        received_json_data=json.loads(request.body)
        idRubrica = int(received_json_data['idRubrica'])
        newNombre = forms.CharField(max_length=50).clean(received_json_data['nombre'])
        newDescripcion = forms.CharField(max_length=50).clean(received_json_data['descripcion'])
        newRubrica = Rubrica.objects.get(pk=idRubrica)
        newRubrica.nombre=newNombre
        newRubrica.descripcion=newDescripcion
        newRubrica.save()

        ##asegurarse que no existen aspectosRubrica asociados
        ##DUDA A FUTURO: ¿porque si elimino primero lso aspectos y despues actualizo la rubrica ,
        ##los aspectos anteriores no se borran?
        AspectoRubrica.objects.filter(rubrica__id=idRubrica).delete()
        
        for i in received_json_data['aspectosRubrica']:
            for elemento in i:
                print(elemento)
                puntaje=float(elemento['puntaje'])
                descripcion=forms.CharField(max_length=50).clean(elemento['descripcion'])
                nombreFila=forms.CharField(max_length=30).clean(elemento['nombreFila'])
                fila=int(elemento['fila'])
                columna=int(elemento['columna'])
                aspectoRubrica = AspectoRubrica(rubrica=newRubrica, 
                                                fila=fila, 
                                                columna=columna,
                                                puntaje=puntaje,
                                                descripcion=descripcion,
                                                nombreFila=nombreFila)
                
                aspectoRubrica.save()

        return HttpResponse('')
    


