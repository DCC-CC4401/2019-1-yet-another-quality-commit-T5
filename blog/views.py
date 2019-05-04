from django.shortcuts import render

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
