from django.shortcuts import render

def post_evaluaciones(request):
    return render(request,'evaluacion/evaluacion_admin.html',{})

def post_evaluacion(request):
    return render(request, 'evaluacion/evaluacion_post.html',{})

def post_postevaluacion(request):
    return render(request, 'evaluacion/postevaluacion.html',{})
