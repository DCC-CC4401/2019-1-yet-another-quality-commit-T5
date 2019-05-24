from django.urls import path
from . import views

urlpatterns = [
    path('evaluaciones', views.post_evaluaciones, name='evaluaciones'),
    path('evaluacion', views.post_evaluacion, name="evaluacion"),
    path('postevaluacion', views.post_postevaluacion, name="post-evaluacion"),
    path('add_evaluacion',views.add_evaluacion, name='add_evaluacion'),
    path('delete_evaluacion', views.delete_evaluacion, name='delete_evaluacion'),
    path(r'evaluaciones/<int:pk>/evaluacion_detalle/', views.evaluacion_detalle, name='evaluacion_detalle'),
]