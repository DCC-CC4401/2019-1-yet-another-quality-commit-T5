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
    Opcionalmente admite los parámetros "grupo, nombre_grupo".
    :param request:
    :return:
    """
    if request.POST \
            and request.FILES['csv_file'] \
            and request.user.groups.filter(name='Profesores').exists():
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.warning(request, 'Debes subir un archivo en formato CSV')
            return HttpResponseRedirect('cursos/' + str(request.POST['id_curso']) + '/curso_detalle')
        try:
            file_data = csv_file.read().decode("utf-8")
            lines = file_data.split("\n")
            for line in lines:
                fields = line.split(",")
                # informacion basica y necesaria para armar un alumno
                data_dict = {}
                data_dict['nombre'] = fields[0]
                data_dict['apellido'] = fields[1]
                data_dict['run'] = fields[2]
                data_dict['correo'] = fields[3]
                data_dict['curso'] = request.POST['id_curso']
                alumno = AlumnoForm(data_dict)
                if alumno.is_valid():
                    alumno.save()
                else:
                    messages.warning(request, 'Formato de alumno no válido')
                # Grupo?
                data_grupo = {}
                try:
                    data_grupo['numero'] = fields[4]
                    # Nombre de grupo?
                    try:
                        data_grupo['nombre'] = fields[5]
                    except Exception as e:
                        pass
                    data_grupo['curso'] = request.POST['id_curso']
                    data_grupo['integrante'] = Alumno.objects.get(run=fields[2], curso=request.POST['id_curso']).pk
                    data_grupo['activo'] = True
                    grupo = GrupoForm(data_grupo)
                    grupo.save()
                except Exception as e:
                    pass
            # cierre de ciclo, todos los alumnos fueron cargados correctamente
            messages.success(request, 'Alumnos cargados correctamente')
            return HttpResponseRedirect('cursos/' + str(request.POST['id_curso']) + '/curso_detalle')
        except Exception as e:
            # se ha levantado una excepcion, los alumnos no estan bien definidos
            messages.warning(request, 'Ha ocurrido un error, no se pudo cargar')
    return HttpResponseRedirect('cursos/' + str(request.POST['id_curso']) + '/curso_detalle')

