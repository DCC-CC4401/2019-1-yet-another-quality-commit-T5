from django import forms
from Rubricas.models import *


class AddRubrica(forms.ModelForm):
    
    class Meta:
        model = Rubrica
        fields = '__all__'