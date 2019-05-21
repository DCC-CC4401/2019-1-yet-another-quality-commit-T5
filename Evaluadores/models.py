from django.core.mail import send_mail
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
        """
        Guarda en la base de datos, y genera un Usuario con privilegios de Evaluador.
        :param args:
        :param kwargs:
        :return:
        """
        # Agrega el modelo a la base de datos
        super(Evaluador, self).save(*args, **kwargs)

        # Genera un User para cada evaluador
        user = str(self.nombre).lower() + "." + str(self.apellido).lower()
        password = User.objects.make_random_password()
        user = User.objects.create_user(username=user,
                                        email=self.correo,
                                        password=password)
        user.first_name = self.nombre
        user.last_name = self.apellido
        # Agrega usuario al grupo Evaluadores
        evaluadores, created = Group.objects.get_or_create(name='Evaluadores')
        evaluadores.user_set.add(user)
        # Guarda usuario
        user.save()
        send_mail('Bienvenido!', 'Tu usuario es: ' + user.username + '\n Tu contraseña es: ' + password, 'djangotesting052@gmail.com',  [self.correo,])

    def update(self, *args, **kwargs):
        """
        Actualiza los datos del evaluador en la base de datos del modelo
        :param args:
        :param kwargs:
        :return:
        """
        super(Evaluador, self).save(*args, **kwargs)


class Profesor(Evaluador):
    """
    Crea un modelo Profesor, y lo guarda como usuario
    """
    def save(self, *args, **kwargs):
        """
        Guarda en la base de datos, y crea un Usuario con privilegios de Profesor.
        :param args:
        :param kwargs:
        :return:
        """
        super(Profesor, self).save(*args, **kwargs)
        profesores, created = Group.objects.get_or_create(name='Profesores')
        user = User.objects.get(email=self.correo)
        profesores.user_set.add(user)