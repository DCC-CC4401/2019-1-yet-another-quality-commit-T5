from django import forms
from Rubricas.models import *


class AddRubrica(forms.Form):
    name = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'class': 'form-control'}))
    descripcion = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                             required=True)
    fila = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'class': 'form-control'}),
                             required=True)
    columna = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'class': 'form-control'}),
                           required=True)
    nombreFila = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'class': 'form-control'}),
                              required=True)

    def is_valid(self):
        return super(AddRubrica,self).is_valid()

    def save(self, *args, **kwargs):
        rubrica=Rubrica(name=self.cleaned_data['name'],
                        descripcion=self.cleaned_data['descripcion'])
        rubrica.save()

        rubricaFinal=AspectoRubrica(rubrica=rubrica.objects.get(id),
                                    fila=self.cleaned_data['fila'],
                                    columna=self.cleaned_data['columna'],
                                    descripcion=rubrica.descripcion,
                                    nombreFila=self.cleaned_data['nombreFila'])

        rubricaFinal.save()