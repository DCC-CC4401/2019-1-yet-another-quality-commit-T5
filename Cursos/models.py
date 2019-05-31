from django.db import models, IntegrityError

from Evaluadores.models import Evaluador


class Curso(models.Model):
    nombre = models.CharField(max_length=40)
    código = models.CharField(max_length=6)
    sección = models.PositiveSmallIntegerField()
    año = models.PositiveSmallIntegerField()
    semestre = models.CharField(max_length=9) #Otoño o Primavera

    class Meta:
        unique_together = ('nombre', 'código', 'sección', 'año', 'semestre')


    def get_pk(self):
        return str(self.pk)

    def get_name(self):
        return str(self.nombre)
    
    def get_code(self):
        return str(self.código)
    
    def get_section(self):
        return str(self.sección)
    
    def get_year(self):
        return str(self.año)

    def get_semester(self):
        return str(self.semestre)

    def get_date(self):
        return str(self.get_semester() +" "+self.get_year())

    def __str__(self):
        return str(self.get_code() + "-" + self.get_section() + " " + self.get_date())


class EvaluadoresCurso(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    evaluador = models.ForeignKey(Evaluador, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('curso', 'evaluador')

    def save(self, *args, **kwargs):
        """
        Guarda el modelo, y agrega todos los nuevos evaluadores a los nuevos cursos.
        :param args:
        :param kwargs:
        :return:
        """
        super(EvaluadoresCurso, self).save(*args, **kwargs)
        from Evaluaciones.models import Evaluacion
        evaluaciones = Evaluacion.objects.filter(curso=self.curso)
        for eval in evaluaciones:
            from Evaluaciones.models import EvaluadoresEvaluacion
            try:
                eval_evaluacion = EvaluadoresEvaluacion(evaluacion=eval, evaluador=self.evaluador)
                eval_evaluacion.save()
            except IntegrityError as e:
                pass

