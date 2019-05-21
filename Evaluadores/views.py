from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
#from django.views.generic.edit import UpdateView

from .models import Evaluador
from .forms import AddEvaluador
from .forms import UpdateEvaluador


def post_evaluadores(request):
    updateForm = UpdateEvaluador()
    addForm = AddEvaluador()
    evaluadores = Evaluador.objects.all()
    evaluadores_list = []

    for evaluador in evaluadores:
        evaluadores_list.append(evaluador)

    #form = AddEvaluador()
    #print(evaluadores_list)
    return render(request, 'evaluadores/evaluadores_admin.html', {'updateForm': updateForm ,'addForm': addForm, 'evaluadores_list': evaluadores_list})


def add_evaluador(request):
    if request.POST:
        form = AddEvaluador(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('evaluadores')
        else:
            form = AddEvaluador()

    return render(request, 'evaluadores/evaluadores_admin.html', {'form': form})



def update_evaluador(request):
    if request.POST:
        addForm = AddEvaluador()
        form = UpdateEvaluador(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('evaluadores')
        else:
            form = UpdateEvaluador()

    return render(request, 'evaluadores/evaluadores_admin.html', {'addForm': addForm, 'updateForm': form})


def delete_evaluador(request):
    if request.POST:
        addForm = AddEvaluador()
        updateForm = UpdateEvaluador()
        id = int(request.POST['ID'])
        user = Evaluador.objects.get(pk=id)
        username = str(user.nombre).lower() + '.' + str(user.apellido).lower()
        User.objects.get(username=username).delete()
        deleted = Evaluador.objects.get(pk=id).delete()
        if(deleted!=None):
            return HttpResponseRedirect('evaluadores')
    return render(request, 'evaluadores/evaluadores_admin.html', {'addForm': addForm, 'updateForm': updateForm})


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
        form = UpdateEvaluador({'ID': id, 'nombre': nombre, 'apellido': apellido, 'correo': correo})
        return render(request, 'evaluadores/profile.html', {'form': form})
    return HttpResponseRedirect('/accounts/login')