from django.urls import path
from . import views

urlpatterns = [
    path(r'cursos/', views.post_cursos, name='cursos'),
    path('add_curso',views.add_curso, name='add_curso'),
    path(r'curso_detalle/<int:pk>', views.curso_detalle, name='curso_detalle'),
]
