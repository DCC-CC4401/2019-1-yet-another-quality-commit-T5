from django.shortcuts import render

def post_cursos(request):
    return render(request,'cursos/cursos_admin.html', {})
