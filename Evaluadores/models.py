from django.db import models

class Evaluador(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.CharField(max_length=50)

    def get_name(self):
        return str(self.nombre + " " + self.apellido)

    def get_email(self):
        return str(self.correo)
