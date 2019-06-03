from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
# from django.views.generic.edit import UpdateView

from .forms import AddCurso, AddGrupo, BoundEvaluador, UpdateGrupo, BoundAlumno
from Evaluaciones.forms import AddEvaluacion
from .models import Curso, EvaluadoresCurso

from Evaluaciones.models import Evaluacion, EvaluadoresEvaluacion

from Alumnos.models import Alumno, Grupo, AlumnosGrupo



@login_required
def post_cursos(request):
    form = AddCurso()
    cursos = Curso.objects.all()

    return render(request, 'cursos/cursos_admin.html', {'form': form, 'cursos_list': cursos})


@login_required
def add_curso(request):
    if request.POST and request.user.groups.filter(name='Profesores').exists():
        form = AddCurso(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Se creo el curso correctamente')
            return HttpResponseRedirect('cursos')
        else:
            form = AddCurso()
    messages.success(request, 'No se pudo crear el curso')
    return HttpResponseRedirect('cursos')


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
    # form para agregar evaluadores al curso
    bound_evaluador = BoundEvaluador({'curso':curso_id})
    # form para agregar evaluaciones al curso
    add_evaluacion = AddEvaluacion({'curso':curso_id})
    #form para agregar grupos al curso
    add_grupo = AddGrupo({'curso':curso_id})
    #form para modificar un grupo
    update_grupo = UpdateGrupo({'curso': curso_id})
    #form para agregar alumnos a un grupo
    bound_alumno = BoundAlumno({'curso': curso_id})

    # lista de evaluadores
    evaluadores = EvaluadoresCurso.objects.filter(curso=curso_id)
    evaluadores_list = []
    for evaluador in evaluadores:
        evaluadores_list.append(evaluador.evaluador)

    # lista de evaluaciones
    evaluaciones = Evaluacion.objects.filter(curso=curso_id)

    # lista de alumnos
    alumnos = Alumno.objects.filter(curso=curso_id)
    # lista de grupos
    grupos = Grupo.objects.filter(curso=curso_id)
    # lista de alumnosgrupos
    listaAlumnosGrupo = []
    for grupo in grupos:
        alumnosGrupo = AlumnosGrupo.objects.filter(grupo=grupo)
        alumnosGrupo_list = []
        for alumno in alumnosGrupo:
            alumnosGrupo_list.append(alumno.integrante)
        listaAlumnosGrupo.append(alumnosGrupo_list)

    return render(request, 'cursos/curso_detalle.html', context={'curso': curso_id,
                                                                 'evaluadores': evaluadores_list,
                                                                 'evaluaciones': evaluaciones,
                                                                 'alumnos': alumnos,
                                                                 'grupos': grupos,
                                                                 'listaAlumnosGrupo': listaAlumnosGrupo,
                                                                 'bound_evaluador': bound_evaluador,
                                                                 'add_evaluacion': add_evaluacion,
                                                                 'add_grupo': add_grupo,
                                                                 'update_grupo': update_grupo,
                                                                 'bound_alumno': bound_alumno})


@login_required
def delete_curso(request):
    if request.POST and request.user.groups.filter(name='Profesores').exists():
        id = int(request.POST.get('id'))
        deleted = Curso.objects.get(pk=id).delete()
        if deleted is not None:
            messages.success(request, 'Curso eliminado correctamente')
            return HttpResponseRedirect('cursos')
    messages.warning(request, 'No se pudo eliminar el curso.')
    return HttpResponseRedirect('cursos')


@login_required
def all_grupos(request):
    from Alumnos.models import Grupo
    grupos = Grupo.objects.all()
    grupos_list = []

    for grupo in grupos:
        grupos_list.append(grupo)

    form = AddGrupo()

    return render(request, 'cursos/cursos_admin.html', {'cursos': grupos_list, 'form': form})


@login_required
def add_grupo(request,pk):
    if request.POST and request.user.groups.filter(name='Profesores').exists():
        form = AddGrupo(request.POST, pk)
        if form.is_valid():
               form.save()
               messages.success(request, 'Grupo creado correctamente')
               return HttpResponseRedirect('/cursos/' + str(pk) + '/curso_detalle')
        messages.warning(request, 'El grupo no pudo ser creado')
        return HttpResponseRedirect('/cursos/' + str(pk) + '/curso_detalle')

@login_required
def delete_grupo(request, pk):
    """
    Elimina un grupo
    :param request:
    :return:
    """
    if request.POST and request.user.groups.filter(name='Profesores').exists():
        id = int(request.POST.get('id'))
        deleted = Grupo.objects.get(pk=id).delete()
        if deleted is not None:
            messages.success(request, 'Grupo eliminado correctamente')
            return HttpResponseRedirect('/cursos/' + str(pk) + '/curso_detalle')
    messages.warning(request, 'El grupo no pudo ser eliminado')
    return HttpResponseRedirect('/cursos/' + str(pk) + '/curso_detalle')

@login_required
def update_grupo(request, pk):
    """
    Actualiza los datos de un grupo, en caso de que la request sea de un Profesor.
    :param request:
    :return:
    """
    if request.POST and request.user.groups.filter(name='Profesores').exists():
        form = UpdateGrupo(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grupo modificado correctamente')
            return HttpResponseRedirect('/cursos/' + str(pk) + '/curso_detalle')
    messages.warning(request, 'El grupo no pudo ser modificado')
    return HttpResponseRedirect('/cursos/' + str(pk) + '/curso_detalle')


@login_required
def bound_evaluador(request, pk):
    """
    Asigna un evaluador a un curso
    :param request:
    :return:
    """
    if request.POST and request.user.groups.filter(name='Profesores').exists():
        form = BoundEvaluador(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Evaluador asignado correctamente')
            return HttpResponseRedirect('/cursos/' + str(pk) + '/curso_detalle')
    messages.warning('El evaluador no pudo ser asignado')
    return HttpResponseRedirect('/cursos/' + str(pk) + '/curso_detalle')


@login_required
def unbound_evaluador(request, pk):
    """
    Retira un evaluador asignado a un curso y de todas las evaluaciones asociadas al curso.
    :param request:
    :return:
    """
    if request.POST and request.user.groups.filter(name='Profesores').exists():
        id_curso = int(request.POST.get('id_curso'))
        id_evaluador = int(request.POST.get('id_evaluador'))
        deleted = EvaluadoresCurso.objects.get(curso=id_curso,
                                               evaluador=id_evaluador).delete()
        evaluaciones_curso = Evaluacion.objects.filter(curso=id_curso)
        for eval in evaluaciones_curso:
            EvaluadoresEvaluacion.objects.filter(evaluacion=eval, evaluador=id_evaluador).delete()
        if deleted is not None:
            messages.success(request, 'Evaluador eliminado correctamente')
            return HttpResponseRedirect('/cursos/' + str(pk) + '/curso_detalle')
    messages.warning('El evaluador no pudo ser eliminado')
    return HttpResponseRedirect('/cursos/' + str(pk) + '/curso_detalle')


@login_required
def add_evaluacion(request, pk):
    """
    Agrega una evaluacion al curso especifico
    :param request:
    :param pk:
    :return:
    """
    if request.POST and request.user.groups.filter(name='Profesores').exists():
        add_evaluacion = AddEvaluacion(request.POST)
        if add_evaluacion.is_valid():
            add_evaluacion.save()
            messages.success(request, 'La evaluación fue agregada correctamente')
            return HttpResponseRedirect('/cursos/' + str(pk) + '/curso_detalle')
    messages.warning(request, 'La evaluación no pudo ser agregada')
    return HttpResponseRedirect('/cursos/' + str(pk) + '/curso_detalle')

@login_required
def bound_alumno(request, pk):
    """
    Asigna un alumno a un grupo
    :param request:
    :return:
    """
    if request.POST and request.user.groups.filter(name='Profesores').exists():
        form = BoundAlumno(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Alumno asignado correctamente')
            return HttpResponseRedirect('/cursos/' + str(pk) + '/curso_detalle')
    messages.warning('El alumno no pudo ser asignado')
    return HttpResponseRedirect('/cursos/' + str(pk) + '/curso_detalle')

@login_required
def unbound_alumno(request, pk):
    """
    Retira un alumno asignado a un grupo
    :param request:
    :return:
    """
    if request.POST and request.user.groups.filter(name='Profesores').exists():
        id_grupo = int(request.POST.get('id_grupo'))
        id_alumno = int(request.POST.get('id_alumno'))
        deleted = AlumnosGrupo.objects.get(grupo=id_grupo, integrante= id_alumno).delete()

        if deleted is not None:
            messages.success(request, 'Alumno eliminado correctamente')
            return HttpResponseRedirect('/cursos/' + str(pk) + '/curso_detalle')
    messages.warning('El alumno no pudo ser eliminado')
    return HttpResponseRedirect('/cursos/' + str(pk) + '/curso_detalle')