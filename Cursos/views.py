from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.edit import UpdateView

from .forms import AddCurso


def post_cursos(request):
    form = AddCurso
    return render(request,'cursos/cursos_admin.html', {'form': form})

def add_curso(request):
    if request.POST:
        form = AddCurso(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('cursos')
        else:
            form = AddCurso

    
    return render(request, 'cursos/cursos_admin.html', {'form': form})