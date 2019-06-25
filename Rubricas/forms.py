from django import forms
from Rubricas.models import Rubrica


class AddRubrica(forms.ModelForm):
    
    class Meta:
        model = Rubrica
        fields = '__all__'
