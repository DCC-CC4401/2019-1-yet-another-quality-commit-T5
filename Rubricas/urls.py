from django.urls import path
from . import views

urlpatterns = [
    path('rubricas', views.post_rubricas, name='rubricas'),
    path('add_rubrica', views.add_rubrica, name='add_rubrica'),
    path('delete_rubrica', views.delete_rubrica, name='delete_rubrica'),
    path('busqueda_rubrica_ajax', views.busqueda_rubrica_ajax),
    path('update_aspectos_rubrica',views.updateAspectosRubrica, name='update_aspectos_rubrica'),
]
