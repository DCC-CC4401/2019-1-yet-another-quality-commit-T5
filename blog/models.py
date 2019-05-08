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

class Rubrica(models.Model):
    name = models.CharField(max_length=50)
    score=models.CharField(max_length=50)
    aspects=models.CharField(max_length=100)
    description=models.TextField()

class Evaluacion(models.Model):
    tiempo_min = models.IntegerField(default=5)
    tiempo_max = models.IntegerField(default=8)
    rubrica = models.ForeignKey(Rubrica, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField(default=timezone.now)
    fecha_fin = models.DateTimeField(default=timezone)
    curso = models.ForeignKey(Course, on_delete=models.CASCADE)
    estado = models.BooleanField(default=False)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Grupo(models.Model):
    nombre = models.CharField(max_length=100)
    curso = models.ForeignKey(Course, on_delete=models.CASCADE)
    






