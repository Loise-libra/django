# core/models.py

from django.db import models
from django.utils import timezone

class Tarea(models.Model):
    nombre = models.CharField(max_length=200)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

    # Esta propiedad nos dará el conteo de acciones que pediste
    @property
    def conteo_acciones(self):
        return self.acciones.count()
    
    # Propiedad para contar acciones completadas
    @property
    def conteo_completadas(self):
        return self.acciones.filter(completada=True).count()

class Accion(models.Model):
    # Relacionamos cada acción con una Tarea
    # related_name='acciones' nos permite usar tarea.acciones.all()
    # on_delete=models.CASCADE significa que si borras una Tarea, sus Acciones se borran.
    tarea = models.ForeignKey(Tarea, related_name='acciones', on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=250)
    completada = models.BooleanField(default=False)

    def __str__(self):
        return self.descripcionhere
