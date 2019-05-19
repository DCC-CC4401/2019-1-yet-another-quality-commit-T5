from django.urls import path
from . import views

urlpatterns = [
    path('rubricas', views.post_rubricas, name='rubricas'),
    path('add_rubrica', views.add_rubrica, name='add_rubrica'),
]
