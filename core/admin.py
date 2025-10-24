# core/admin.py

from django.contrib import admin
from .models import Tarea, Accion

# Esto permite ver las acciones dentro del detalle de la Tarea
class AccionInline(admin.TabularInline):
    model = Accion
    extra = 1 # Cuántos campos vacíos mostrar

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_creacion', 'conteo_acciones')
    inlines = [AccionInline]

# También registramos Accion por separado (opcional)
@admin.register(Accion)
class AccionAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'tarea', 'completada')
    list_filter = ('completada', 'tarea')