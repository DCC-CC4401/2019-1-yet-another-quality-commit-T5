from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('cursos', views.post_cursos, name='cursos'),
]