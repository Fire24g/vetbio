from django.contrib import admin
from .models import Responsable, Maquina, Mantencion


@admin.register(Responsable)
class ResponsableAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'apellido', 'rut', 'email')


@admin.register(Maquina)
class MaquinaAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'tipo', 'estado')
	list_filter = ('estado',)


@admin.register(Mantencion)
class MantencionAdmin(admin.ModelAdmin):
	list_display = ('id_maquina', 'id_responsable', 'fecha')
	list_select_related = ('id_maquina', 'id_responsable')
