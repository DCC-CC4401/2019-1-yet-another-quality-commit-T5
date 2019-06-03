from django.shortcuts import render

def post_list(request):
    return render(request, 'evaluadores/landing_page_eval.html', {})
