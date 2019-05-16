from django.urls import path
from . import views

urlpatterns = [
    path('rubricas', views.post_rubricas, name='rubricas'),
]