from django import forms
from Evaluadores.models import *


class AddEvaluador(forms.Form):

    Nombre = forms.CharField(max_length=50,
                           widget=forms.TextInput(attrs={'class': 'form-control'}),
                           required=True)
    Apellido = forms.CharField(max_length=50,
                           widget=forms.TextInput(attrs={'class': 'form-control'}),
                           required=True)
    Email = forms.EmailField(required=True)

    def is_valid(self):
        return super(AddEvaluador, self).is_valid()


    def save(self, *args, **kwargs):
        evaluador = Evaluador(nombre=self.cleaned_data['Nombre'],
                              apellido=self.cleaned_data['Apellido'],
                              correo=self.cleaned_data['Email'])

        evaluador.save()