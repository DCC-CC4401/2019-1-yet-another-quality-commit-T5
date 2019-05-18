from django.shortcuts import render
from django.http import HttpResponseRedirect
from Evaluaciones.forms import *

def post_evaluaciones(request):
    return render(request,'evaluacion/evaluacion_admin.html',{})

def post_evaluacion(request):
    return render(request, 'evaluacion/evaluacion_post.html',{})

def post_postevaluacion(request):
    return render(request, 'evaluacion/postevaluacion.html',{})

def add_evaluacion(request):
    if request.POST:
        form = AddEvaluacion(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('add_evaluacion')
        else:
            form = AddEvaluacion()

        return render(request, 'evaluacion/evaluacion_admin.html', {'form': form})
