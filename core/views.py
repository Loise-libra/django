# core/views.py

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Tarea, Accion
import json

# Vista Principal: Carga la página HTML y las tareas iniciales
def lista_tareas(request):
    # Lógica del buscador
    query = request.GET.get('q', '')
    if query:
        tareas = Tarea.objects.filter(nombre__icontains=query).order_by('-fecha_creacion')
    else:
        tareas = Tarea.objects.all().order_by('-fecha_creacion')
    
    # Pasamos las tareas al template
    return render(request, 'core/lista_tareas.html', {'tareas': tareas})


# --- VISTAS DE API (para JavaScript) ---

# API: Crear una nueva tarea
def api_crear_tarea(request):
    if request.method == 'POST':
        # Decodificamos los datos JSON que envía JavaScript
        data = json.loads(request.body)
        nombre_tarea = data.get('nombre')
        
        if nombre_tarea:
            tarea = Tarea.objects.create(nombre=nombre_tarea)
            # Devolvemos la nueva tarea como JSON
            return JsonResponse({
                'id': tarea.id,
                'nombre': tarea.nombre,
                'fecha_creacion': tarea.fecha_creacion.strftime('%d/%m/%Y'),
                'conteo_acciones': 0
            }, status=201)
    return JsonResponse({'error': 'Petición inválida'}, status=400)

# API: Eliminar una tarea
def api_eliminar_tarea(request, tarea_id):
    if request.method == 'POST': # Usamos POST para eliminar por seguridad
        try:
            tarea = Tarea.objects.get(id=tarea_id)
            tarea.delete()
            return JsonResponse({'success': True})
        except Tarea.DoesNotExist:
            return JsonResponse({'error': 'Tarea no encontrada'}, status=404)
    return JsonResponse({'error': 'Petición inválida'}, status=400)

# API: Agregar una acción a una tarea
def api_agregar_accion(request, tarea_id):
    if request.method == 'POST':
        try:
            tarea = Tarea.objects.get(id=tarea_id)
            data = json.loads(request.body)
            desc_accion = data.get('descripcion')
            
            if desc_accion:
                accion = Accion.objects.create(tarea=tarea, descripcion=desc_accion)
                return JsonResponse({
                    'id': accion.id,
                    'descripcion': accion.descripcion,
                    'completada': accion.completada
                }, status=201)
        except Tarea.DoesNotExist:
            return JsonResponse({'error': 'Tarea no encontrada'}, status=404)
    return JsonResponse({'error': 'Petición inválida'}, status=400)

# API: Marcar/Desmarcar una acción (el "check")
def api_toggle_accion(request, accion_id):
    if request.method == 'POST':
        try:
            accion = Accion.objects.get(id=accion_id)
            # Invertimos el estado 'completada'
            accion.completada = not accion.completada
            accion.save()
            return JsonResponse({
                'id': accion.id,
                'completada': accion.completada
            })
        except Accion.DoesNotExist:
            return JsonResponse({'error': 'Acción no encontrada'}, status=404)
    return JsonResponse({'error': 'Petición inválida'}, status=400)

# Esta función maneja la nueva página de "Detalle de Tarea"
def detalle_tarea(request, tarea_id):
    # Obtenemos la tarea específica por su ID.
    # Si no la encuentra, mostrará un error 404.
    tarea = get_object_or_404(Tarea, id=tarea_id)
    
    # Pasamos esa tarea a una nueva plantilla
    return render(request, 'core/tarea_detalle.html', {'tarea': tarea})