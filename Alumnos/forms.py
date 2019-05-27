from django import forms
from Alumnos.models import Alumno
from Alumnos.models import Grupos


class AlumnoForm(forms.ModelForm):

    class Meta:
        model = Alumno
        fields = '__all__'


class GrupoFrom(forms.ModelForm):

    class Meta:
        model = Grupos
        fields= '__all__'

