from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from random import shuffle

from django.core.exceptions import ObjectDoesNotExist

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
        idGrupo = int(request.POST['idGrupo'])
        idCurso = int(request.POST['idCurso'])
        grupo = Grupo.objects.get(pk=idGrupo)
        evaluador= Evaluador.objects.get(correo=request.user.username)
        evaluacion=Evaluacion.objects.get(pk=idEvaluacion)
        rubrica = evaluacion.rubrica
        aspectos = AspectoRubrica.objects.filter(rubrica=rubrica)
        aspectos = aspectos.order_by('fila','columna')
        grouped = []
        ##en caso de ser admin se obtienen los otros evaluadores y se revisa si ya entregaron alguna evaluacion
        if request.user.groups.filter(name='Profesores').exists():
            evaluadores = EvaluadoresEvaluacion.objects.filter(evaluacion=evaluacion)
            yaEvaluaron = []
            for evaluadorAux in evaluadores:
                if(FichaEvaluacion.objects.filter(evaluador=evaluadorAux.evaluador, evaluacion=evaluacion).exists()):
                    yaEvaluaron.append(evaluadorAux.evaluador)
                    
            
            

            

            ##luego revisar que alumnos del grupo ya ha presentado

            ##TODO filtro temporal puesto que aun no se hace lo de grupos
            alumnos = Alumno.objects.filter(curso_id=idCurso)
            evaluaciones = Evaluacion.objects.filter(curso_id=idCurso)
            presentadores = []
            for alumno in alumnos:
                for evaluacionAux in evaluaciones:
                    if(FichaEvaluacion.objects.filter(evaluacion=evaluacionAux, presentador=alumno).exists()):
                        presentadores.append(alumno)
                        break



        ##ahora agrupamos por fila, la salida es [[aspectosfila1][aspectosfila2][...]]
        for aspecto in aspectos:
            if (len(grouped)-1 < aspecto.fila):
                grouped.append([])
            grouped[aspecto.fila].append(aspectoRubrica_serializer(aspecto))

        ##esto es para obtener las respuestas anteriores del evaluador
        try:
            ficha = FichaEvaluacion.objects.get(evaluacion=evaluacion, grupo=grupo, evaluador=evaluador )
            presentador = ficha.presentador
            groupedRespuestas = []
            respuestasBDD = EvaluacionAspectos.objects.filter(fichaEvaluacion=ficha)
        
            for respuesta in respuestasBDD:
                groupedRespuestas.append(respuesta_serializer(respuesta))
        except ObjectDoesNotExist:
            ficha=None
            presentador=None
            groupedRespuestas=[]



        data={'alumnos':alumnos,'evaluacion':evaluacion,'grupo':grupo, 'detalleRubrica':json.dumps(grouped), 'respuestas': json.dumps(groupedRespuestas), 'presentador':presentador, 'evaluadores':evaluadores, 'yaPresentaron':presentadores, 'yaEvaluaron':yaEvaluaron}
        
        
        return render(request, 'evaluacion/evaluacion_evaluar.html', data)

def respuesta_serializer(evaluacionAspecto):
    return {'fila':evaluacionAspecto.aspectoRubrica.fila, 'columna':evaluacionAspecto.aspectoRubrica.columna}

def aspectoRubrica_serializer(aspectoRubrica):
    return {'fila': aspectoRubrica.fila, 'columna' : aspectoRubrica.columna,
                'puntaje': str(aspectoRubrica.puntaje), 'nombreFila':aspectoRubrica.nombreFila,
                    'descripcion': aspectoRubrica.descripcion}


@login_required
def send_evaluacion(request):
    if request.method == "POST":

        grupo=Grupo.objects.get(pk=int(request.POST['idGrupo']))
        evaluacion=Evaluacion.objects.get(pk=int(request.POST['idEvaluacion']))
        rubrica=evaluacion.rubrica
        evaluador=Evaluador.objects.get(correo=request.user.username)
        hora=None
        minutos=None
        presentador=None

        if request.user.groups.filter(name='Profesores').exists():
            hora=int(request.POST['hora'])
            minutos=int(request.POST['minutos'])
            presentador=Alumno.objects.get(pk=int(request.POST['presentador']))
        
        fichaEvaluacion,created = FichaEvaluacion.objects.get_or_create(evaluacion=evaluacion,
                                                                evaluador=evaluador,
                                                                grupo=grupo,
                                                                defaults={'estado_grupo':'N/A',
                                                                'estado_evaluacion':'N/A',
                                                                'tiempo':10,
                                                                'presentador':presentador})
        if not created:
            fichaEvaluacion.estado_grupo='N/A'
            fichaEvaluacion.estado_evaluacion='N/A'
            fichaEvaluacion.tiempo=10
            fichaEvaluacion.presentador=presentador
        fichaEvaluacion.save()

        EvaluacionAspectos.objects.filter(fichaEvaluacion=fichaEvaluacion).delete()
        
        for elemento in json.loads(request.POST['respuestas']):
            print(elemento)
            aspectoRubrica= AspectoRubrica.objects.get(fila=int(elemento['fila']), 
                                        columna=int(elemento['columna']),
                                            rubrica=rubrica)
            respuesta=EvaluacionAspectos(fichaEvaluacion=fichaEvaluacion, aspectoRubrica=aspectoRubrica)
            respuesta.save()
        
        return post_postevaluacion(request=request)
            
            
        


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

import json
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
    curso_id= Evaluacion.objects.get(pk=pk).curso.get_pk()
    grupos = Grupo.objects.filter(curso=curso_id).order_by('?')
    rubrica_id=Evaluacion.objects.get(pk=pk).rubrica.pk
    rubrica_nombre=Rubrica.objects.get(pk=rubrica_id).nombre
    rubrica_descripcion=Rubrica.objects.get(pk=rubrica_id).descripcion
    rubrica_aspecto=[]
    rubricas=AspectoRubrica.objects.filter(rubrica=rubrica_id)
    rubricas=rubricas.order_by('fila','columna')
    for r in rubricas:
        if (len(rubrica_aspecto) - 1 < r.fila):
            rubrica_aspecto.append([])
        rubrica_aspecto[r.fila].append(aspectoRubrica_serializer(r))
    for eval in evaluadores_raw:
        evaluadores.append(eval.evaluador)
    evaluador_form = BoundEvaluador({'evaluacion' : evaluacion_id})
    return render(request, 'evaluacion/evaluacion_detalle.html', context={'evaluacion':evaluacion_id, 'evaluador_form' : evaluador_form, 'evaluadores' : evaluadores, 'grupos':grupos,
                                                                          'rubrica':rubrica_id,
                                                                          'rubrica_aspecto':rubrica_aspecto,
                                                                          'rubrica_nombre': rubrica_nombre,
                                                                          'rubrica_descripcion': rubrica_descripcion})


import json


def busqueda_rubrica_ajax(request,pk):
    if request.GET:
        id_rubrica = request.GET['id']
        aspectos = AspectoRubrica.objects.filter(rubrica__id=id_rubrica)
        aspectos = aspectos.order_by('fila', 'columna')
        grouped = []
        ##ahora agrupamos por fila, la salida es [[aspectosfila1][aspectosfila2][...]]
        for aspecto in aspectos:
            if (len(grouped) - 1 < aspecto.fila):
                grouped.append([])
            grouped[aspecto.fila].append(aspectoRubrica_serializer(aspecto))

        return HttpResponse(json.dumps(grouped), content_type='application/json')


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

def evaluar(request,grupopk,evalpk):
    grupo_id=Grupo.objects.get(pk=grupopk)
    curso_id=Grupo.objects.get(pk=grupopk).curso.get_pk()
    evaluacion_id=Evaluacion.objects.get(pk=evalpk)
    evaluadores_raw = EvaluadoresEvaluacion.objects.filter(evaluacion=evaluacion_id)
    evaluadores = []
    for eval in evaluadores_raw:
        evaluadores.append(eval.evaluador)
    evaluador_form = BoundEvaluador({'evaluacion': evaluacion_id})
    return render(request, 'evaluacion/evaluacion_grupo.html',
                  context={'grupo': grupo_id, 'curso': curso_id,
                           'evaluacion':evaluacion_id,
                           'evaluadores': evaluadores,
                           'evaluador_form':evaluador_form})

def curso_unbound_evaluador(request,evalpk, grupopk):
    if request.POST:
        id_evaluacion = int(request.POST.get('id_evaluacion'))
        id_evaluador = int(request.POST.get('id_evaluador'))
        deleted = EvaluadoresEvaluacion.objects.get(evaluacion=id_evaluacion,
                                                    evaluador=id_evaluador).delete()
        if deleted is not None:
            return HttpResponseRedirect('/evaluaciones/' + str(evalpk) +'/'+ str(grupopk)+'/evaluacion_evaluar')
    return HttpResponseRedirect('/evaluaciones/' + str(evalpk)+'/'+str(grupopk) + '/evaluacion_evaluar')

def curso_bound_evaluador(request, evalpk, grupopk):
    if request.POST:
        evaluacion = request.POST['id_evaluacion']
        evaluador = request.POST['evaluador']
        form = BoundEvaluador({'evaluacion':evaluacion, 'evaluador':evaluador})
        if form.is_valid():
            form.save()
            messages.success(request, 'Se ha vinculado al evaluador correctamente')
            return HttpResponseRedirect('/evaluaciones/' + str(evalpk) +'/'+ str(grupopk)+ '/evaluacion_evaluar')
    messages.warning(request, 'No se pudo vincular al evaluador')
    return HttpResponseRedirect('/evaluaciones/' + str(evalpk) +'/'+ str(grupopk)+ '/evaluacion_evaluar')

def comenzar_evaluacion(request, grupopk, evalpk):
     id_grupo=Grupo.objects.get(pk=grupopk)
     id_evaluacion=Evaluacion.objects.get(pk=evalpk)
     return render(request, 'evaluacion/evaluacion_evaluar.html',
                   context={'grupo':id_grupo,
                            'evaluacion':id_evaluacion})


def updateAspectosRubrica(request,pk):
    if request.method == "POST":
        received_json_data = json.loads(request.body)
        idRubrica = int(received_json_data['idRubrica'])
        newNombre = forms.CharField(max_length=50).clean(received_json_data['nombre'])
        newDescripcion = forms.CharField(max_length=50).clean(received_json_data['descripcion'])
        newRubrica = Rubrica.objects.get(pk=idRubrica)
        newRubrica.nombre = newNombre
        newRubrica.descripcion = newDescripcion
        newRubrica.save()

        ##asegurarse que no existen aspectosRubrica asociados
        ##DUDA A FUTURO: ¿porque si elimino primero lso aspectos y despues actualizo la rubrica ,
        ##los aspectos anteriores no se borran?
        AspectoRubrica.objects.filter(rubrica__id=idRubrica).delete()

        for i in received_json_data['aspectosRubrica']:
            for elemento in i:
                print(elemento)
                puntaje = float(elemento['puntaje'])
                descripcion = forms.CharField(max_length=50).clean(elemento['descripcion'])
                nombreFila = forms.CharField(max_length=30).clean(elemento['nombreFila'])
                fila = int(elemento['fila'])
                columna = int(elemento['columna'])
                aspectoRubrica = AspectoRubrica(rubrica=newRubrica,
                                                fila=fila,
                                                columna=columna,
                                                puntaje=puntaje,
                                                descripcion=descripcion,
                                                nombreFila=nombreFila)

                aspectoRubrica.save()

        return HttpResponse('')

