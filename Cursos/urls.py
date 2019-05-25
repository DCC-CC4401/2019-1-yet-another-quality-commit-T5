from django.urls import path
from . import views

urlpatterns = [
    path(r'cursos/', views.post_cursos, name='cursos'),
    path('add_curso',views.add_curso, name='add_curso'),
    path('delete_curso', views.delete_curso, name='delete_curso'),
    path(r'cursos/<int:pk>/curso_detalle/', views.curso_detalle, name='curso_detalle'),
    path(r'cursos/<int:pk>/agregar_grupo/', views.add_grupo, name='add_grupo'),
]
