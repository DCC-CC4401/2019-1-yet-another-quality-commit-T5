from django import forms
from Alumnos.models import Alumno
from Alumnos.models import Grupo


class AlumnoForm(forms.ModelForm):

    class Meta:
        model = Alumno
        fields = '__all__'


class GrupoFrom(forms.ModelForm):

    class Meta:
        model = Grupo
        fields= '__all__'

