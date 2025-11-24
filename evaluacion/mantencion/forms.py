from django import forms
from .models import Responsable, Maquina, Mantencion


class ResponsableForm(forms.ModelForm):
    class Meta:
        model = Responsable
        fields = ['nombre', 'apellido', 'rut', 'email', 'telefono', 'especialidad']


class MaquinaForm(forms.ModelForm):
    class Meta:
        model = Maquina
        fields = ['nombre', 'tipo', 'estado']


class MantencionForm(forms.ModelForm):
    class Meta:
        model = Mantencion
        fields = ['id_maquina', 'id_responsable', 'fecha', 'descripcion']
