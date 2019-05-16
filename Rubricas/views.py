from django.shortcuts import render

def post_rubricas(request):
    return render(request,'rubrica/rubrica_admin.html', {})
