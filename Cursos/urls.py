from django.urls import path
from . import views

urlpatterns = [
    path('cursos', views.post_cursos, name='cursos'),
]
