from django.db import models
from django.utils import timezone
from django.conf.urls import url
from django.contrib import admin


class Evaluador(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.CharField(max_length=50)

    def get_name(self):
        return str(self.nombre + " " + self.apellido)

    def get_email(self):
        return str(self.correo)

class Curso(models.Model):
    nombre = models.CharField(max_length=40)
    código = models.CharField(max_length=6)
    sección = models.CharField(max_length=1)
    año = models.PositiveSmallIntegerField()
    semestre = models.CharField(max_length=9) #Otoño o Primavera

class Rubrica(models.Model):
    name = models.CharField(max_length=50)
    score=models.CharField(max_length=50)
    aspects=models.CharField(max_length=100)
    description=models.TextField()

class Evaluación(models.Model):
    tiempo_min = models.IntegerField(default=5)
    tiempo_max = models.IntegerField(default=8)
    rubrica = models.ForeignKey(Rubrica, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField(timezone.now())
    fecha_fin = models.DateTimeField(timezone.now())
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    estado = models.BooleanField(default=False)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Grupo(models.Model):
    nombre = models.CharField(max_length=100)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)


class Alumno(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    rut = models.CharField(max_length=12)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=30)


class FichaEvaluacion(models.Model):
    evaluacion = models.ForeignKey(Evaluación, on_delete=models.CASCADE)
    evaluador = models.ForeignKey(Evaluador, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    estado_grupo = models.CharField(max_length=15)
    estado_evaluacion = models.CharField(max_length=15)
    tiempo = models.IntegerField(default=0)
    presentador = models.ForeignKey(Alumno, on_delete=models.CASCADE)


    






