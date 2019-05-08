from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('cursos', views.post_cursos, name='cursos'),
    path('evaluadores', views.post_evaluadores, name='evaluadores'),
    path('rubricas', views.post_rubricas, name='rubricas'),
    path('evaluaciones', views.post_evaluaciones, name='evaluaciones'),
    path('evaluacion', views.post_evaluacion, name="evaluacion"),
    path('postevaluacion', views.post_postevaluacion, name="post-evaluacion")
]
