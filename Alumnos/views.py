import csv
import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from Alumnos.forms import *


# Create your views here.
from Cursos.models import Curso


@login_required
def add_alumno(request):
    if request.POST and request.user.groups.filter(name='Profesores').exists():
        form = AlumnoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('cursos')

    return post_alumnos(request)

@login_required
def post_alumnos(request):
    form = AlumnoForm()
    alumnos = Alumno.objects.all()
    alumnos_list = []

    for alumno in alumnos:
        alumnos_list.append(alumno)

    return render(request, 'cursos/cursos_admin.html', {'form': form, 'alumno_list': alumnos_list})


@login_required
def upload_data(request):
    """
    Carga un archivo CSV con los datos de los alumnos
    Se espera que el archivo tenga el formato "nombre, apellido, run, correo"
    :param request:
    :return:
    """
    if request.POST and request.FILES['csv_file']:
        csv_file = request.FILES["csv_file"]
        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")
        for line in lines:
            fields = line.split(",")
            data_dict = {}
            data_dict['nombre'] = fields[0]
            data_dict['apellido'] = fields[1]
            data_dict['run'] = fields[2]
            data_dict['correo'] = fields[3]
            data_dict['curso'] = request.POST['id_curso']
            print(data_dict)
            alumno = AlumnoForm(data_dict)
            alumno.save()
    return HttpResponseRedirect('cursos')