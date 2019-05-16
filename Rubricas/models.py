from django.db import models

class Rubrica(models.Model):
    name = models.CharField(max_length=50)
    descripcion = models.CharField(default="", max_length=50)


class AspectoRubrica(models.Model):
    rubrica = models.ForeignKey(Rubrica, on_delete=models.CASCADE)
    fila = models.IntegerField(default=0)
    columna = models.IntegerField(default=0)
    puntaje = models.DecimalField(default=0, max_digits=1, decimal_places=1)
    nombreFila = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=50)



