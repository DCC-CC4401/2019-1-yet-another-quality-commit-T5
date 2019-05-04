from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Evaluacion(models.Model):
    tiempo_min = models.IntegerField(default=5)
    tiempo_max = models.CharField(default=8)
    rubrica = models.ForeignKey(Rubrica, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField(default=timezone.now)
    fecha_fin = models.DateTimeField(default=timezone)
    curso = models.ForeignKey(Curso, onde_delete=models.CASCADE)
    estado = models.BooleanField(default=False)
