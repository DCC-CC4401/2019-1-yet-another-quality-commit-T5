from django.db import models

class Rubrica(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(default="", max_length=50)

    def __str__(self):
        return str(self.pk) + " "+ self.nombre

    def save(self, *args, **kwargs):
        """
        Guarda en la base de datos, y crea sus aspectos de rubrica básicos.
        :param args:
        :param kwargs:
        :return:
        """
        super(Rubrica, self).save(*args, **kwargs)
        AspectoRubrica(rubrica=self,fila=0,columna=0,puntaje=0.0, nombreFila= "Aspecto 1", descripcion="Nivel 1").save()
        AspectoRubrica(rubrica=self,fila=0,columna=1,puntaje=2.0, nombreFila= "Aspecto 1", descripcion="Nivel 2").save()
        AspectoRubrica(rubrica=self,fila=0,columna=2,puntaje=4.0, nombreFila= "Aspecto 1", descripcion="Nivel 3").save()
        AspectoRubrica(rubrica=self,fila=1,columna=0,puntaje=0.0, nombreFila= "Aspecto 2", descripcion="Nivel 1").save()
        AspectoRubrica(rubrica=self,fila=1,columna=1,puntaje=1.5, nombreFila= "Aspecto 2", descripcion="Nivel 2").save()
        AspectoRubrica(rubrica=self,fila=1,columna=2,puntaje=3.0, nombreFila= "Aspecto 2", descripcion="Nivel 3").save()


class AspectoRubrica(models.Model):
    rubrica = models.ForeignKey(Rubrica, on_delete=models.CASCADE)
    fila = models.IntegerField(default=0)
    columna = models.IntegerField(default=0)
    puntaje = models.DecimalField(default=0, max_digits=2, decimal_places=1)
    nombreFila = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return str(self.rubrica.pk) +" "+ str(self.fila)+ "__"+str(self.columna)

    
    



