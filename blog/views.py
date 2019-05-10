from django.http import HttpResponseRedirect
from django.shortcuts import render

from blog.forms import AddEvaluador


def post_list(request):
    return render(request, 'blog/post_list.html', {})

def post_cursos(request):
    return render(request,'blog/cursos.html', {})


def post_evaluadores(request):
    return render(request,'blog/evaluadores.html', {})

def post_rubricas(request):
    return render(request,'blog/rubricas.html', {})

def post_evaluaciones(request):
    return render(request,'blog/evaluaciones.html',{})

def post_evaluacion(request):
    return render(request, 'blog/evaluacion.html',{})
def post_postevaluacion(request):
    return render(request, 'blog/postevaluacion.html',{})


def add_evaluador(request):
    if request.method == 'POST':
        form = AddEvaluador(request.POST)
        if form.is_valid():
            new_persona = form.save()
            new_persona.save()
            return HttpResponseRedirect('blog/evaluadores.html')
    else:
        form = AddEvaluador()

    return render(request, 'blog/evaluadores.html', {})

