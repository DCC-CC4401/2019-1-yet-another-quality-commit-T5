from django.db import models
from django.utils import timezone
from Cursos.models import Curso, Alumno, Grupo
from Rubricas.models import Rubrica
from Rubricas.models import AspectoRubrica
from Evaluadores.models import Evaluador


class Evaluacion(models.Model):
    tiempo_min = models.PositiveSmallIntegerField(default=5)
    tiempo_max = models.PositiveSmallIntegerField(default=8)
    #rubrica = models.ForeignKey(Rubrica, on_delete=models.CASCADE)
    fecha_inicio = models.DateField(default=timezone.now)
    fecha_fin = models.DateField(default=timezone.now)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    estado = models.CharField(max_length=7) # Abierta o Cerrada
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    def get_rank(self):
        return str(self.tiempo_min) + "-" + str(self.tiempo_max) + " min"

    def get_startdate(self):
        return str(self.fecha_inicio)

    def get_enddate(self):
        return str(self.fecha_fin)

    def get_course(self):
        return str(self.curso)

    def get_state(self):
        return str(self.estado)


class FichaEvaluacion(models.Model):
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE)
    evaluador = models.ForeignKey(Evaluador, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    estado_grupo = models.CharField(max_length=15)
    estado_evaluacion = models.CharField(max_length=15)
    tiempo = models.IntegerField(default=0)
    presentador = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    rubrica = models.ForeignKey(AspectoRubrica, on_delete=models.CASCADE)

    def get_evaluation(self):
        return str(self.evaluacion)

    def get_evaluator(self):
        return str(self.evaluador)

    def get_group(self):
        return str(self.grupo)

    def get_groupstatus(self):
        return str(self.estado_grupo)

    def get_evaluationstatus(self):
        return str(self.estado_evaluacion)

    def get_time(self):
        return str(self.tiempo)

    def get_presenter(self):
        return str(self.presentador)
