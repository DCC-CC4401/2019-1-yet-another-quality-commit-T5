from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from Evaluaciones.forms import *
from django.template import Context, Template

@login_required
def post_evaluaciones(request):
    """
    Vista principal de evaluaciones, que incluye todas las evaluaciones insistentes y formulario de agregar evaluaciones.
    :param request:
    :return:
    """
    form = AddEvaluacion()
    evaluaciones = Evaluacion.objects.all().order_by('fecha_fin')
    # mostrar solo las 10 ultimas
    evaluaciones = evaluaciones[:10]
    return render(request, 'evaluacion/evaluacion_admin.html', {'form': form, 'evaluacion_list': evaluaciones})


@login_required
def post_postevaluacion(request):
    return render(request, 'evaluacion/postevaluacion.html',{})

import json

@login_required
def post_evaluacion(request):
    if request.POST:
        idEvaluacion=int(request.POST['idEvaluacion'])
        print(idEvaluacion)
        rubrica = Evaluacion.objects.get(pk=idEvaluacion).rubrica
        aspectos = AspectoRubrica.objects.filter(rubrica=rubrica)
        aspectos = aspectos.order_by('fila','columna')
        grouped = []
        ##ahora agrupamos por fila, la salida es [[aspectosfila1][aspectosfila2][...]]
        for aspecto in aspectos:
            if (len(grouped)-1 < aspecto.fila):
                grouped.append([])
            grouped[aspecto.fila].append(aspectoRubrica_serializer(aspecto))

        data={'idEvaluacion':idEvaluacion, 'detalleRubrica':json.dumps(grouped)}
    
        
        return render(request, 'evaluacion/evaluacion_evaluar.html', data)



def aspectoRubrica_serializer(aspectoRubrica):
    return {'fila': aspectoRubrica.fila, 'columna' : aspectoRubrica.columna,
                'puntaje': str(aspectoRubrica.puntaje), 'nombreFila':aspectoRubrica.nombreFila,
                    'descripcion': aspectoRubrica.descripcion}




@login_required()
def add_evaluacion(request):
    """
    Agrega una evaluacion, en caso de que la request sea de un profesor.
    :param request:
    :return:
    """
    if request.POST and request.user.groups.filter(name='Profesores').exists():
        form = AddEvaluacion(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('evaluaciones')
    return HttpResponseRedirect('evaluaciones')


@login_required
def all_evaluaciones(request):
    """
    Despliega las evaluaciones existentes en la plataforma.
    :param request:
    :return:
    """
    evaluaciones = Evaluacion.objects.all()
    evaluacion_list = []

    for evaluacion in evaluaciones:
        evaluacion_list.append(evaluacion)

    form = AddEvaluacion()

    return render(request, 'evaluacion/evaluacion_admin.html', {'evaluacion': evaluacion_list, 'form':form})


@login_required
def evaluacion_detalle(request, pk):
    """
    Muestra el detalle de la evaluacion pk
    :param request:
    :param pk:
    :return:
    """
    evaluacion_id=Evaluacion.objects.get(pk=pk)
    evaluadores_raw = EvaluadoresEvaluacion.objects.filter(evaluacion=evaluacion_id)
    evaluadores = []
    for eval in evaluadores_raw:
        evaluadores.append(eval.evaluador)
    evaluador_form = BoundEvaluador({'evaluacion' : evaluacion_id})
    return render(request, 'evaluacion/evaluacion_detalle.html', context={'evaluacion':evaluacion_id, 'evaluador_form' : evaluador_form, 'evaluadores' : evaluadores})


@login_required
def delete_evaluacion(request):
    """
    Elimina una evaluacion
    :param request:
    :return:
    """
    if request.POST and request.user.groups.filter(name='Profesores').exists():
        id = int(request.POST.get('id'))
        deleted = Evaluacion.objects.get(pk=id).delete()
        if deleted is not None:
            return HttpResponseRedirect('evaluaciones')
    return HttpResponseRedirect('evaluaciones')


@login_required
def bound_evaluador(request, pk):
    """
    Asigna un evaluador a una evaluacion
    :param request:
    :return:
    """
    if request.POST and request.user.groups.filter(name='Profesores').exists():
        evaluacion = request.POST['id_evaluacion']
        evaluador = request.POST['evaluador']
        form = BoundEvaluador({'evaluacion':evaluacion, 'evaluador':evaluador})
        if form.is_valid():
            form.save()
            messages.success(request, 'Se ha vinculado al evaluador correctamente')
            return HttpResponseRedirect('/evaluaciones/' + str(pk) + '/evaluacion_detalle')
    messages.warning(request, 'No se pudo vincular al evaluador')
    return HttpResponseRedirect('/evaluaciones/' + str(pk) + '/evaluacion_detalle')


@login_required
def unbound_evaluador(request, pk):
    """
    Retira un evaluador asignado a una evaluacion
    :param request:
    :return:
    """
    if request.POST and request.user.groups.filter(name='Profesores').exists():
        id_evaluacion = int(request.POST.get('id_evaluacion'))
        id_evaluador = int(request.POST.get('id_evaluador'))
        deleted = EvaluadoresEvaluacion.objects.get(evaluacion=id_evaluacion,
                                                    evaluador=id_evaluador).delete()
        if deleted is not None:
            return HttpResponseRedirect('/evaluaciones/' + str(pk) + '/evaluacion_detalle')
    return HttpResponseRedirect('/evaluaciones/' + str(pk) + '/evaluacion_detalle')

def evaluar(request,pk):
    evaluacion_id = Evaluacion.objects.get(pk=pk)
    return render(request, 'evaluacion/evaluacion_evaluar.html',
                  context={'evaluacion': evaluacion_id})