from django.contrib import admin
from .models import Curso, Rubrica, Evaluador, Evaluación


admin.site.register(Curso)
admin.site.register(Evaluador)
admin.site.register(Rubrica)
admin.site.register(Evaluación)