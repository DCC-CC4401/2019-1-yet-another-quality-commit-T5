from django.shortcuts import render
from django.http import HttpResponseRedirect
from Evaluaciones.forms import *

def post_evaluaciones(request):
    form = AddEvaluacion()
    evaluaciones = Evaluacion.objects.all()
    evaluacion_list = []

    for evaluacion in evaluaciones:
        evaluacion_list.append(evaluacion)

    return render(request, 'evaluacion/evaluacion_admin.html', {'form': form, 'evaluacion_list': evaluacion_list})

def post_evaluacion(request):
    return render(request, 'evaluacion/evaluacion_post.html',{})

def post_postevaluacion(request):
    return render(request, 'evaluacion/postevaluacion.html',{})

def add_evaluacion(request):
    if request.POST:
        form = AddEvaluacion(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('evaluacion')
        else:
            form = AddEvaluacion()

        return render(request, 'evaluacion/evaluacion_admin.html', {'form': form})

def all_evaluaciones(request):
    evaluaciones = Evaluacion.objects.all()
    evaluacion_list = []

    for evaluacion in evaluaciones:
        evaluacion_list.append(evaluacion)

    form = AddEvaluacion()

    return render(request, 'evaluacion/evaluacion_admin.html', {'evaluacion': evaluacion_list, 'form':form})

def evaluacion_detalle(request, pk):
    evaluacion_id=Evaluacion.objects.get(pk=pk)
    return render(request, 'evaluacion/evaluacion_detalle.html', context={'evaluacion':evaluacion_id})