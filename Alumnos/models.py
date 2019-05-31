from django.db import models
from Cursos.models import Curso
# Create your models here.


class Alumno(models.Model):

    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    run = models.IntegerField()
    correo = models.EmailField(max_length=50)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['run', 'curso']

    def __str__(self):
        return str(self.nombre) + ' ' + str(self.apellido)


class Grupo(models.Model):

    numero = models.IntegerField(default=0)
    nombre = models.CharField(max_length=30, blank=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    integrante = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)

    def __str__(self):
        if self.nombre:
            return str(self.numero) + ' - ' + str(self.nombre)
        return str(self.numero)