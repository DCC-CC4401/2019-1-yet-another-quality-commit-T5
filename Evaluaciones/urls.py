from django.urls import path
from . import views

urlpatterns = [
    path('evaluaciones', views.post_evaluaciones, name='evaluaciones'),
    path('evaluacion', views.post_evaluacion, name="evaluacion"),
    path('postevaluacion', views.post_postevaluacion, name="post-evaluacion")
]