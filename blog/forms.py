from django import forms
from blog.models import *

class AddEvaluadorForm(forms.Form):

    name = forms.CharField(max_length=50,
                           widget=forms.TextInput(attrs={'class': 'form-control'}),
                           required=True)
    lastname = forms.CharField(max_length=50,
                           widget=forms.TextInput(attrs={'class': 'form-control'}),
                           required=True)
    email = forms.EmailField(required=True)

    def is_valid(self):
        return super(AddEvaluadorForm, self).is_valid()


    def save(self, *args, **kwargs):
        evaluador = Evaluador(nombre=self.cleaned_data['name'],
                              apellido=self.cleaned_data['lastname'],
                              correo=self.cleaned_data['email'])

        evaluador.save()

class AddCursoForm(forms.Form):
    nombre = forms.CharField(max_length=40,
                             widget=forms.TextInput(attrs={'class': 'form-control'}),
                             required=True)
    codigo = forms.CharField(max_length=6,
                             widget=forms.TextInput(attrs={'class': 'form-control'}),
                             required=True)
    seccion = forms.CharField(max_length=1,
                              widget=forms.Select(attrs={'class': 'form-control'}),
                              required=True)
    anno = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                             required=True)
    semestre = forms.ChoiceField(choices=['Otoño','Primavera'],
                                widget=forms.Select(attrs={'class': 'form-control'}),
                                required=True)

    def is_valid(self):
        return super(AddCursoForm, self).is_valid()


    def save(self, *args, **kwargs):
        curso = Curso(nombre=self.cleaned_data['nombre'],
                      código=self.cleaned_data['codigo'],
                      sección=self.cleaned_data['seccion'],
                      año=self.cleaned_data['anno'],
                      semestre=self.cleaned_data['semestre'])

        curso.save()


