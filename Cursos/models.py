from django.db import models

class Curso(models.Model):
    nombre = models.CharField(max_length=40)
    codigo = models.CharField(max_length=6)
    seccion = models.CharField(max_length=1)
    año = models.PositiveSmallIntegerField()
    semestre = models.CharField(max_length=9) #Otoño o Primavera

class Grupo(models.Model):
    nombre = models.CharField(max_length=100)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

class Alumno(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    rut = models.CharField(max_length=12)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=30)
