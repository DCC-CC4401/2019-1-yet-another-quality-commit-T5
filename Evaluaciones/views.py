from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from Evaluaciones.forms import *


@login_required
def post_evaluaciones(request):
    """
    Vista principal de evaluaciones, que incluye todas las evaluaciones insistentes y formulario de agregar evaluaciones.
    :param request:
    :return:
    """
    form = AddEvaluacion()
    evaluaciones = Evaluacion.objects.all().order_by('fecha_fin')
    evaluacion_list = []

    for evaluacion in evaluaciones:
        evaluacion_list.append(evaluacion)

    return render(request, 'evaluacion/evaluacion_admin.html', {'form': form, 'evaluacion_list': evaluacion_list})


@login_required
def post_evaluacion(request):
    return render(request, 'evaluacion/evaluacion_post.html',{})


@login_required
def post_postevaluacion(request):
    return render(request, 'evaluacion/postevaluacion.html',{})


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
            return HttpResponseRedirect('evaluacion')
        else:
            form = AddEvaluacion()
            return render(request, 'evaluacion/evaluacion_admin.html', {'form': form})
    return post_evaluaciones(request)


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
    evaluacion_id=Evaluacion.objects.get(pk=pk)
    return render(request, 'evaluacion/evaluacion_detalle.html', context={'evaluacion':evaluacion_id})


@login_required
def delete_evaluacion(request):
    if request.POST:
        id = int(request.POST.get('id'))
        deleted = Evaluacion.objects.get(pk=id).delete()
        if deleted is not None:
            return HttpResponseRedirect('evaluacion')
    return post_evaluaciones(request)