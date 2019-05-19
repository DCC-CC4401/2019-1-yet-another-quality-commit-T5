from django import forms
from Evaluadores.models import *


class AddEvaluador(forms.ModelForm):

    class Meta:
        model = Evaluador
        fields = '__all__'


class UpdateEvaluador(forms.ModelForm):

    ID = forms.CharField(widget=forms.TextInput(attrs={'readonly':'', 'size':'4'}),required=True)
    
    class Meta:
        model = Evaluador
        fields = ['ID','nombre','apellido','correo']

    def save(self, *args, **kwargs):
        id = int(self.cleaned_data['ID'])
        evaluador = Evaluador.objects.get(pk=id)
        #change name
        evaluador.nombre = self.cleaned_data['nombre']
        evaluador.apellido = self.cleaned_data['apellido']
        evaluador.correo  = self.cleaned_data['correo']
        evaluador.save()