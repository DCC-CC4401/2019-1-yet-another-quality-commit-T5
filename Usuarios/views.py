from django.shortcuts import render

def post_list(request):
    return render(request, 'landing_page1.html', {})
