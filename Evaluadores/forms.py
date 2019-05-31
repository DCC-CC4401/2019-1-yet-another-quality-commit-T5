from django import forms
from Evaluadores.models import *


class AddEvaluador(forms.ModelForm):

    class Meta:
        model = Evaluador
        fields = '__all__'


class UpdateEvaluador(forms.ModelForm):

    ID = forms.CharField(widget=forms.TextInput(attrs={'readonly':'', 'size':'4','style':'display:none'}),required=True)
    
    class Meta:
        model = Evaluador
        fields = ['ID','nombre','apellido','correo']

    def save(self, *args, **kwargs):
        # obtener evaluador
        id = int(self.cleaned_data['ID'])
        evaluador = Evaluador.objects.get(pk=id)
        # obtener su perfil de usuario
        username = str(evaluador.nombre).lower() + "." + str(evaluador.apellido).lower()
        user = User.objects.get(username=username)

        # actualizar informacion database
        evaluador.nombre = self.cleaned_data['nombre']
        evaluador.apellido = self.cleaned_data['apellido']
        evaluador.correo  = self.cleaned_data['correo']
        evaluador.update()

        # actualizar informacion de usuario
        user.username = str(evaluador.nombre).lower() + "." + str(evaluador.apellido).lower()
        user.first_name = evaluador.nombre
        user.last_name = evaluador.apellido
        user.email = evaluador.correo
        user.save()


class AddProfesor(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = '__all__'


