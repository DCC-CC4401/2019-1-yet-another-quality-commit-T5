from django.db import models
from django.utils import timezone

from Alumnos.models import Grupo, Alumno
from Cursos.models import Curso, EvaluadoresCurso
from Rubricas.models import Rubrica
from Rubricas.models import AspectoRubrica
from Evaluadores.models import Evaluador


class Evaluacion(models.Model):
    tiempo_min = models.PositiveSmallIntegerField(default=5)
    tiempo_max = models.PositiveSmallIntegerField(default=8)
    rubrica = models.ForeignKey(Rubrica, on_delete=models.CASCADE, null=True, blank=True)
    fecha_inicio = models.DateField(default=timezone.now)
    fecha_fin = models.DateField(default=timezone.now)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    estado = models.CharField(max_length=7) # Abierta o Cerrada
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    def get_pk(self):
        return str(self.pk)

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

    def is_active(self):
        return self.get_state()=="Abierta"

    def get_rubrica(self):
        return str(self.rubrica)

    def save(self, *args, **kwargs):
        """
        Guarda el modelo y asigna todos los evaluadores del curso
        :param args:
        :param kwargs:
        :return:
        """
        super(Evaluacion, self).save(*args, **kwargs)

        evaluadores = EvaluadoresCurso.objects.filter(curso=self.curso)
        for eval in evaluadores:
            eval_eval = EvaluadoresEvaluacion(evaluacion=self, evaluador=eval.evaluador)
            eval_eval.save()


class FichaEvaluacion(models.Model):
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE)
    evaluador = models.ForeignKey(Evaluador, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    estado_grupo = models.CharField(max_length=15)
    estado_evaluacion = models.CharField(max_length=15)
    tiempo = models.IntegerField(default=0)
    presentador = models.ForeignKey(Alumno, on_delete=models.CASCADE, null=True, blank=True)
    

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


class EvaluadoresEvaluacion(models.Model):
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE)
    evaluador = models.ForeignKey(Evaluador, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('evaluacion', 'evaluador')

class EvaluacionAspectos(models.Model):
    fichaEvaluacion = models.ForeignKey(FichaEvaluacion, on_delete=models.CASCADE)
    aspectoRubrica = models.ForeignKey(AspectoRubrica, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('fichaEvaluacion', 'aspectoRubrica')
    
class GrupoEvaluacion(models.Model):
    grupo= models.ForeignKey(Grupo, on_delete=models.CASCADE)
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE)
    abierto=models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('grupo', 'evaluacion')
