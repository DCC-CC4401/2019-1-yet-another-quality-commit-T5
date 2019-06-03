from django.urls import path
from . import views

urlpatterns = [
    path(r'cursos/', views.post_cursos, name='cursos'),
    path('add_curso',views.add_curso, name='add_curso'),
    path('delete_curso', views.delete_curso, name='delete_curso'),
    path(r'cursos/<int:pk>/curso_detalle/', views.curso_detalle, name='curso_detalle'),
    path(r'cursos/<int:pk>/agregar_grupo/', views.add_grupo, name='add_grupo'),
    path(r'cursos/<int:pk>/delete_grupo/', views.delete_grupo, name='delete_grupo'),
    path(r'cursos/<int:pk>/update_grupo', views.update_grupo, name='update_grupo'),
    path('cursos/<int:pk>/bound_evaluador/', views.bound_evaluador, name='bound_evaluador'),
    path('cursos/<int:pk>/unbound_evaluador/', views.unbound_evaluador, name='unbound_evaluador'),
    path('cursos/<int:pk>/add_evaluacion/', views.add_evaluacion, name='add_evaluacion'),
    path('cursos/<int:pk>/bound_alumno/', views.bound_alumno, name='bound_alumno'),
    path('cursos/<int:pk>/unbound_alumno/', views.unbound_alumno, name='unbound_alumno'),
    path(r'cursos/<int:pk>/edit_grupo', views.edit_grupo, name='edit_grupo'),
]
