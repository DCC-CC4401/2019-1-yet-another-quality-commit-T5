from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=40)
    code = models.CharField(max_length=6)
    section = models.CharField(max_length=1)
    year = models.PositiveSmallIntegerField()
    semester = models.CharField(max_length=9) #Otoño o Primavera

class Grupo(models.Model):
    nombre = models.CharField(max_length=100)
    curso = models.ForeignKey(Course, on_delete=models.CASCADE)

class Alumno(models.Model):
    curso = models.ForeignKey(Course, on_delete=models.CASCADE)
    rut = models.CharField(max_length=12)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=30)
