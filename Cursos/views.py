from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
# from django.views.generic.edit import UpdateView

from .forms import AddCurso
from .models import Curso


@login_required
def post_cursos(request):
    form = AddCurso()
    cursos = Curso.objects.all()
    cursos_list = []

    for curso in cursos:
        cursos_list.append(curso)

    return render(request, 'cursos/cursos_admin.html', {'form': form, 'cursos_list': cursos_list})


@login_required
def add_curso(request):
    if request.POST and request.user.groups.filter(name='Profesores').exists():
        form = AddCurso(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('cursos')
        else:
            form = AddCurso()

    return post_cursos(request)


@login_required
def all_cursos(request):
    cursos = Curso.objects.all()
    cursos_list = []

    for curso in cursos:
        cursos_list.append(curso)

    form = AddCurso()

    return render(request, 'cursos/cursos_admin.html', {'cursos': cursos_list, 'form': form})


@login_required
def curso_detalle(request, pk):
    curso_id = Curso.objects.get(pk=pk)
    return render(request, 'cursos/curso_detalle.html', context={'curso': curso_id})


@login_required
def delete_curso(request):
    if request.POST:
        id = int(request.POST.get('id'))
        deleted = Curso.objects.get(pk=id).delete()
        if deleted is not None:
            return HttpResponseRedirect('cursos')
    return post_cursos(request)