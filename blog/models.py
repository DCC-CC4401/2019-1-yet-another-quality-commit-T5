from django.db import models
from django.utils import timezone
from django.conf.urls import url
from django.contrib import admin


class Evaluador(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.CharField(max_length=50)

    def get_name(self):
        return str(self.nombre + " " + self.correo)


class Course(models.Model):
    name = models.CharField(max_length=40)
    code = models.CharField(max_length=6)
    section = models.CharField(max_length=1)
    year = models.PositiveSmallIntegerField()
    semester = models.CharField(max_length=9) #Otoño o Primavera

