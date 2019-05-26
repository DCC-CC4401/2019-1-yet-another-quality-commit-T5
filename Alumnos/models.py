from django.db import models
# Create your models here.


class Alumno(models.Model):

    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    run = models.IntegerField(primary_key=True)
    correo = models.EmailField(max_length=50)


class Grupos(models.Model):

    nombre = models.CharField(max_length=30)
    integrante = models.ForeignKey(Alumno, on_delete=models.CASCADE)