from django.urls import path
from . import views

urlpatterns = [
    path('evaluaciones', views.post_evaluaciones, name='evaluaciones'),
    path('evaluacion', views.post_evaluacion, name="evaluacion"),
    path('postevaluacion', views.post_postevaluacion, name="post-evaluacion"),
    path('add_evaluacion',views.add_evaluacion, name='add_evaluacion'),
    path('delete_evaluacion', views.delete_evaluacion, name='delete_evaluacion'),
    path('evaluaciones/<int:pk>/bound_evaluador/', views.bound_evaluador, name='bound_evaluador'),
    path('evaluaciones/<int:pk>/unbound_evaluador/', views.unbound_evaluador, name='unbound_evaluador'),
    path(r'evaluaciones/<int:pk>/evaluacion_detalle/', views.evaluacion_detalle, name='evaluacion_detalle'),
    path(r'evaluaciones/<int:grupopk>/<int:evalpk>/evaluacion_evaluar/', views.evaluar, name='evaluar'),
    path(r'evaluaciones/<int:grupopk>/<int:evalpk>/unbond_evaluador', views.curso_unbound_evaluador, name='curso_unbound_evaluador'),
    path(r'evaluaciones/<int:grupopk>/<int:evalpk>/bond_evaluador', views.curso_bound_evaluador, name='curso_bound_evaluador'),
]