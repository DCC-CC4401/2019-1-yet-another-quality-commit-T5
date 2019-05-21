from django import template
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='is_evaluador')
def is_evaluador(user):
    """
    Devuelve True si corresponde a un Usuario con privilegios de Evaluador
    :param value:
    :param arg:
    :return:
    """
    return user.groups.filter(name='Evaluadores').exists()


@register.filter(name='is_admin')
def is_admin(user):
    """
    Devuelve True si corresponde a un Usuario con privilegios de Administrador
    :param user:
    :return:
    """
    return user.groups.filter(name='Profesores').exists()