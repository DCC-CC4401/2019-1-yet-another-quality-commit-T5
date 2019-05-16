from django.db import models
from django.utils import timezone
from Cursos.models import Course, Alumno, Grupo
from Rubricas.models import Rubrica
from Rubricas.models import AspectoRubrica
from Evaluadores.models import Evaluador


class Evaluacion(models.Model):
    tiempo_min = models.IntegerField(default=5)
    tiempo_max = models.IntegerField(default=8)
    rubrica = models.ForeignKey(Rubrica, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField(timezone.now())
    fecha_fin = models.DateTimeField(timezone.now())
    curso = models.ForeignKey(Course, on_delete=models.CASCADE)
    estado = models.BooleanField(default=False)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class FichaEvaluacion(models.Model):
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE)
    evaluador = models.ForeignKey(Evaluador, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    estado_grupo = models.CharField(max_length=15)
    estado_evaluacion = models.CharField(max_length=15)
    tiempo = models.IntegerField(default=0)
    presentador = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    rubrica = models.ForeignKey(AspectoRubrica, on_delete=models.CASCADE)
