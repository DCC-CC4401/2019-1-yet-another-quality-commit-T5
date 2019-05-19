from django.db import models

class Evaluador(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.EmailField(max_length=50)
    creado = models.DateTimeField(auto_now=True)

    def get_name(self):
        return str(self.nombre)

    def get_lastname(self):
        return str(self.apellido)

    def get_email(self):
        return str(self.correo)

    def get_pk(self):
        return str(self.pk)

    def __str__(self):
        return str(self.nombre + " " + self.apellido)
    
