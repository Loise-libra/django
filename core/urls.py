# core/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # La página principal
    path('', views.lista_tareas, name='lista_tareas'),
    
    # --- PÁGINA NUEVA ---
    # Esta es la nueva URL para ver el detalle de UNA tarea
    path('tarea/<int:tarea_id>/', views.detalle_tarea, name='detalle_tarea'),
    
    # --- RUTAS DE LA API (para JavaScript) ---
    path('api/tarea/crear/', views.api_crear_tarea, name='api_crear_tarea'),
    path('api/tarea/<int:tarea_id>/eliminar/', views.api_eliminar_tarea, name='api_eliminar_tarea'),
    path('api/tarea/<int:tarea_id>/agregar_accion/', views.api_agregar_accion, name='api_agregar_accion'),
    path('api/accion/<int:accion_id>/toggle/', views.api_toggle_accion, name='api_toggle_accion'),
]