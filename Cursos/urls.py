from django.urls import path
from . import views

urlpatterns = [
    path('cursos', views.post_cursos, name='cursos'),
    path('add_curso',views.add_curso, name='add_curso'),
    path('curso_detalle', views.curso_detalle, name='curso_detalle'),
]
