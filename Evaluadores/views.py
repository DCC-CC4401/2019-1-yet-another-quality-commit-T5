from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
#from django.views.generic.edit import UpdateView

from .models import Evaluador
from .models import Profesor
from .forms import AddEvaluador, AddProfesor
from .forms import UpdateEvaluador


@login_required
def post_evaluadores(request):
    """
    Vista del panel de evaluadores, permite su modificacion por parte de usuarios con privilegios
    :param request:
    :return:
    """
    # lista de evaluadores
    evaluadores = Evaluador.objects.all()
    evaluadores_list = []

    for evaluador in evaluadores:
        evaluadores_list.append(evaluador)

    # si el usuario es un profesor, cargar formularios de adicion y edicion de evaluadores
    if request.user.groups.filter(name='Profesores').exists():
        updateForm = UpdateEvaluador()
        addForm = AddEvaluador()
        # devolver la lista de evaluadores y los formularios
        return render(request, 'evaluadores/evaluadores_admin.html', {'updateForm': updateForm ,'addForm': addForm, 'evaluadores_list': evaluadores_list})
    # devolver la lista de evaluadores
    return render(request, 'evaluadores/evaluadores_admin.html', {'evaluadores_list': evaluadores_list})


@login_required
def add_evaluador(request):
    """
    Agrega un evaluador, en caso de que la request sea de un Profesor.
    Caso contrario, redirige a la vista de evaluaciones.
    :param request: request
    :return:
    """
    if request.POST and request.user.groups.filter(name='Profesores').exists():
        #verificar si ya existe usuario
        usuarios=Evaluador.objects.filter(correo=request.POST['correo'])
        if usuarios.count() > 0:
            ##caso en que existe mas de un usuario con el mismo email
            messages.warning(request, 'El email ya está en uso')
            return HttpResponseRedirect('evaluadores')

        form = AddEvaluador(request.POST)
        if form.is_valid():
            form.save()
            ##caso exitoso
            messages.success(request, 'Evaluador agregado correctamente')
            return HttpResponseRedirect('evaluadores')
        else:
            form = AddEvaluador()
        
            

    return post_evaluadores(request)
    
    


@login_required
def update_evaluador(request):
    """
    Actualiza los datos de un Evaluador, en caso de que la request sea de un Profesor.
    :param request:
    :return:
    """
    if request.POST:
        addForm = AddEvaluador()
        form = UpdateEvaluador(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('evaluadores')
    addForm = AddEvaluador()
    form = UpdateEvaluador()
    return render(request, 'evaluadores/evaluadores_admin.html', {'addForm': addForm, 'updateForm': form})


@login_required
def delete_evaluador(request):
    """
    Elimina a un Evaluador.
    :param request:
    :return:
    """
    if request.POST and request.user.groups.filter(name='Profesores').exists():
        addForm = AddEvaluador()
        updateForm = UpdateEvaluador()
        id = int(request.POST['ID'])
        user = Evaluador.objects.get(pk=id)
        username = user.correo
        User.objects.get(username=username).delete()
        deleted = Evaluador.objects.get(pk=id).delete()
        if(deleted!=None):
            return HttpResponseRedirect('evaluadores')
    return render(request, 'evaluadores/evaluadores_admin.html', {'addForm': addForm, 'updateForm': updateForm})


@login_required
def get_evaluador_profile(request):
    """
    Recupera la informacion del Evaluador, y le permite modificador
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        nombre = request.user.first_name
        apellido = request.user.last_name
        correo = request.user.email
        id = Evaluador.objects.get(correo=correo).id
        passwordForm = PasswordChangeForm(request.user)
        form = UpdateEvaluador({'ID': id, 'nombre': nombre, 'apellido': apellido, 'correo': correo})
        return render(request, 'evaluadores/profile.html', {'form': form, 'passwordForm' : passwordForm})
    return HttpResponseRedirect('login')


#@login_required
def add_profesor(request):

    """
    Agrega un Profesor, en caso de que el usuario de la request sea un Profesor.
    :param request:
    :return:
    """
    if request.POST: # temporalmente, sin restricciones
        
        #verificar si ya existe usuario
        usuarios=Evaluador.objects.filter(correo=request.POST['correo'])
        if usuarios.count() > 0:
            ##caso en que existe mas de un usuario con el mismo email
            messages.warning(request, 'El email ya está en uso')
            return HttpResponseRedirect('evaluadores')
        
        form = AddProfesor(request.POST)
        if form.is_valid():
            form.save()
            ##caso exitoso
            messages.success(request, 'Evaluador agregado correctamente')
            return HttpResponseRedirect('evaluadores')
        else:
            form = AddProfesor()
            return render(request, 'evaluadores/evaluadores_admin.html', {'form': form})
    return post_profesores(request)


#@login_required
def post_profesores(request):
    """
    Despliega los profesores registrados en la plataforma.
    Requiere de un usuario loggeado.
    :param request:
    :return:
    """
    addForm = AddProfesor()
    profesores = Profesor.objects.all()
    profesores_list = []

    for profesor in profesores:
        profesores_list.append(profesor)

    #form = AddEvaluador()
    #print(evaluadores_list)
    return render(request, 'contacto.html', {'addForm': addForm, 'profesores_list': profesores_list})