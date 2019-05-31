from django import template
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='group_filter')
def group_filter(grupos, alumno):
    """
    Devuelve el grupo de un alumno, partiendo de una lista de alumnos filtrada por curso
    :param grupos: lista de grupos de un curso especifico (curso_detalle)
    :param alumno: alumno a consultar grupo
    :return:
    """
    try:
        grupo = grupos.get(integrante=alumno, activo=True)
        return grupo
    except Exception as e:
        return 'No asignado'