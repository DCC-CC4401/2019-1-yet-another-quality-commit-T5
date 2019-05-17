from django import forms
from Cursos.models import *

class AddCurso(forms.Form):
    Nombre = forms.CharField(max_length=40,
                             widget=forms.TextInput(attrs={'class': 'form-control'}),
                             required=True)
    Código = forms.CharField(max_length=6,
                             widget=forms.TextInput(attrs={'class': 'form-control'}),
                             required=True)
    
    Año = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                             required=True)
    
    Sección = forms.IntegerField(max_value=10,min_value=0,
                              widget=forms.widgets.NumberInput(attrs={'class': 'form-control'}),
                              required=True)
    Semestre = forms.ChoiceField(choices=(("Otoño","Otoño"),("Primavera","Primavera")),
                                widget=forms.Select(attrs={'class': 'form-control'}),
                                required=True)

    def is_valid(self):
        return super(AddCurso, self).is_valid()


    def save(self, *args, **kwargs):
        curso = Curso(nombre=self.cleaned_data['Nombre'],
                      codigo=self.cleaned_data['Código'],
                      seccion=self.cleaned_data['Sección'],
                      año=self.cleaned_data['Año'],
                      semestre=self.cleaned_data['Semestre'])

        curso.save()