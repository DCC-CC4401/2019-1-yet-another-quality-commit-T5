from django import forms
from Cursos.models import *
from Alumnos.models import Grupo, Alumno, AlumnosGrupo

class AddCurso(forms.Form):

    Nombre = forms.CharField(max_length=40,
                             widget=forms.TextInput(attrs={'class': 'form-control'}),
                             required=True)
    Código = forms.CharField(max_length=6,
                             widget=forms.TextInput(attrs={'class': 'form-control'}),
                             required=True)

    Año = forms.IntegerField(max_value=2100, min_value=2019,
                             widget=forms.NumberInput(attrs={'class': 'form-control'}),
                             required=True)

    Sección = forms.IntegerField(max_value=10, min_value=0,
                                 widget=forms.widgets.NumberInput(attrs={'class': 'form-control'}),
                                 required=True)
    Semestre = forms.ChoiceField(choices=(("Otoño", "Otoño"), ("Primavera", "Primavera")),
                                 widget=forms.Select(attrs={'class': 'form-control'}),
                                 required=True)

    def is_valid(self):
        return super(AddCurso, self).is_valid()

    def save(self, *args, **kwargs):
        curso = Curso(nombre=self.cleaned_data['Nombre'],
                      código=self.cleaned_data['Código'],
                      sección=self.cleaned_data['Sección'],
                      año=self.cleaned_data['Año'],
                      semestre=self.cleaned_data['Semestre'])

        curso.save()

class AddGrupo(forms.Form):
    Número = forms.IntegerField(min_value=1, max_value=20,
                                widget=forms.NumberInput(attrs={'class': 'form-control'}),
                                required=True)
    Nombre = forms.CharField(max_length=50,
                             widget=forms.TextInput(attrs={'class': 'form-control'}),
                             required=False)
    Curso = forms.ModelChoiceField(queryset=Curso.objects,
                                   widget=forms.Select(attrs={'class':'form-control'}),
                                   label='Curso')
    #Integrante = forms.ModelChoiceField(queryset=Alumno.objects,
                                   #widget=forms.Select(attrs={'class':'form-control'}),
                                   #label='Integrante')
    Activo = forms.ChoiceField(choices=(("Activo", "Sí"), ("No activo", "No")),
                               widget=forms.Select({'class': 'form-control'}),
                               required=True)

    def is_valid(self):
        return super(AddGrupo,self).is_valid()

    def save(self, *args, **kwargs):
        grupo=Grupo(numero=self.cleaned_data['Número'],
                    nombre=self.cleaned_data['Nombre'],
                    curso=self.cleaned_data['Curso'],
                    #integrante=self.cleaned_data['Integrante'],
                    activo=self.cleaned_data['Activo'])

        grupo.save()


class UpdateGrupo(forms.Form):

    ID = forms.CharField(widget=forms.TextInput(attrs={'readonly': '', 'size': '4'}), required=True)

    Nombre = forms.CharField(max_length=50,
                             widget=forms.TextInput(attrs={'class': 'form-control'}),
                             required=True)
    Activo = forms.ChoiceField(choices=(("Activo", "Sí"), ("No activo", "No")),
                               widget=forms.Select({'class': 'form-control'}),
                               required=True)

    def save(self, *args, **kwargs):
        # obtener grupo
        id = int(self.cleaned_data['ID'])
        grupo = Grupo.objects.get(pk=id)

        # actualizar informacion database
        grupo.nombre = self.cleaned_data['Nombre']
        grupo.activo = self.cleaned_data['Activo']
        grupo.update()


class BoundEvaluador(forms.ModelForm):

    class Meta:
        model = EvaluadoresCurso
        fields = '__all__'

class BoundAlumno(forms.ModelForm):

    class Meta:
        model = AlumnosGrupo
        fields = '__all__'
