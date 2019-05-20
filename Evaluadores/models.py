from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


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

    def save(self, *args, **kwargs):
        # Agrega el modelo a la base de datos
        super(Evaluador, self).save(*args, **kwargs)

        # Genera un User
        user = str(self.nombre).lower() + "." + str(self.apellido).lower()
        password = User.objects.make_random_password()
        user = User.objects.create_user(username=user,
                                        email=self.correo,
                                        password=password)
        user.first_name = self.nombre
        user.last_name = self.apellido

        evaluadores = Group.objects.get(name='Evaluadores')
        evaluadores.user_set.add(user)

        user.save()