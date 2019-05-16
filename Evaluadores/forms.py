from django import forms
from Evaluadores.models import *


class AddEvaluador(forms.ModelForm):

    class Meta:
        model = Evaluador
        fields = '__all__'
