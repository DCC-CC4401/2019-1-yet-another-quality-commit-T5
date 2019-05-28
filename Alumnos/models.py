from django.db import models
# Create your models here.


class Alumno(models.Model):

    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    run = models.IntegerField(primary_key=True, unique=True)
    correo = models.EmailField(max_length=50)

    def __str__(self):
        return str(self.nombre) + ' ' + str(self.apellido)


class Grupo(models.Model):

    nombre = models.CharField(max_length=30)
    integrante = models.ForeignKey(Alumno, on_delete=models.CASCADE)


class HistoricoGrupo(models.Model):
    """
    Usar para guardar informacion de los grupos NO activos.
    """
    nombre = models.CharField(max_length=30)
    integrante = models.ForeignKey(Alumno, on_delete=models.CASCADE)