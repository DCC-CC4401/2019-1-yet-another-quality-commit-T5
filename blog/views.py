from django.http import HttpResponseRedirect
from django.shortcuts import render

from blog.forms import AddEvaluadorForm, AddCursoForm
from blog.models import Evaluador, Curso


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

def all_evaluadores(request):
    evaluadores = Evaluador.objects.all()
    evaluadores_list = []

    for evaluador in evaluadores:
        evaluadores_list.append(evaluador)

    form = AddEvaluadorForm()

    return render(request, 'blog/evaluadores.html', {'evaluadores': evaluadores_list, 'form':form})


def add_evaluador(request):
    if request.POST:
        form = AddEvaluadorForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            #new_persona = form.save()
            #new_persona.save()
            return HttpResponseRedirect('blog/evaluadores.html')
    #else:
        #form = AddEvaluadorForm()

    return render(request, 'blog/evaluadores.html', {})

def all_cursos(request):
    cursos = Curso.objects.all()
    cursos_list = []

    for curso in cursos:
        cursos_list.append(curso)

    form = AddCursoForm()

    return render(request, 'blog/cursos.html', {'cursos': cursos_list, 'form':form})


def add_curso(request):
    if request.POST:
        form = AddCursoForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('blog/cursos.html')

    return render(request, 'blog/cursos.html', {})
