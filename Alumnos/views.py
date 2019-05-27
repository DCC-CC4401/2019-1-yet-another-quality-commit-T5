from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from Alumnos.forms import *


# Create your views here.
@login_required
def add_alumno(request):
    if request.POST and request.user.groups.filter(name='Profesores').exists():
        form = AlumnoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('cursos')
        else:
            form = AlumnoForm()

    return post_alumnos(request)


def post_alumnos(request):
    form = AlumnoForm()
    alumnos = Alumno.objects.all()
    alumnos_list = []

    for alumno in alumnos:
        alumnos_list.append(alumno)

    return render(request, 'cursos/cursos_admin.html', {'form': form, 'alumno_list': alumnos_list})
