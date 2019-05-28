from django import forms
from Cursos.models import *

class AddCurso(forms.Form):

    Nombre = forms.CharField(max_length=40,
                             widget=forms.TextInput(attrs={'class': 'form-control'}),
                             required=True)
    Código = forms.CharField(max_length=6,
                             widget=forms.TextInput(attrs={'class': 'form-control'}),
                             required=True)

    Año = forms.IntegerField(max_value=2100, min_value=2019,
                             widget=forms.NumberInput(attrs={'class': 'form-control'}),
                             required=True)

    Sección = forms.IntegerField(max_value=10, min_value=0,
                                 widget=forms.widgets.NumberInput(attrs={'class': 'form-control'}),
                                 required=True)
    Semestre = forms.ChoiceField(choices=(("Otoño", "Otoño"), ("Primavera", "Primavera")),
                                 widget=forms.Select(attrs={'class': 'form-control'}),
                                 required=True)

    def is_valid(self):
        return super(AddCurso, self).is_valid()

    def save(self, *args, **kwargs):
        curso = Curso(nombre=self.cleaned_data['Nombre'],
                      código=self.cleaned_data['Código'],
                      sección=self.cleaned_data['Sección'],
                      año=self.cleaned_data['Año'],
                      semestre=self.cleaned_data['Semestre'])

        curso.save()

class AddGrupo(forms.Form):
    Lista_alumnos=("Alumno1", "Alumno2", "Alumno3", "Alumno4")
    Nombre = forms.CharField(max_length=40,
                             widget=forms.TextInput(attrs={'class': 'form-control'}),
                             required=True)

    def is_valid(self):
        return super(AddGrupo,self).is_valid()

    def save(self, *args, **kwargs):
        grupo=Grupo(nombre=self.cleaned_data['Nombre'])

        grupo.save()


class BoundEvaluador(forms.ModelForm):

    class Meta:
        model = EvaluadoresCurso
        fields = '__all__'


