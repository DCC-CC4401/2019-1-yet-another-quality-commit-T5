from django import forms
from blog.models import *

class AddEvaluador(forms.Form):

    name = forms.CharField(max_length=50,
                           widget=forms.TextInput(attrs={'class': 'form-control'}),
                           required=True)
    lastname = forms.CharField(max_length=50,
                           widget=forms.TextInput(attrs={'class': 'form-control'}),
                           required=True)
    email = forms.CharField(max_length=50,
                           widget=forms.TextInput(attrs={'class': 'form-control'}),
                           required=True)

    def save(self, *args, **kwargs):
        evaluador = Evaluador(name=self.cleaned_data['name'],
                              lastname=self.cleaned_data['lastname'],
                              email=self.cleaned_data['email'])

        evaluador.save()