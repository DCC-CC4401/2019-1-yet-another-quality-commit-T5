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

class Evaluador(models.Model):
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    mail = models.CharField(max_length=50)

    def get_name(self):
        return str(self.name + " " + self.lastname)


class Course(models.Model):
    name = models.CharField(40)
    code = models.CharField(6)
    section = models.CharField(1)
    year = models.PositiveSmallIntegerField()
    semester = models.CharField(9) #Otoño o Primavera