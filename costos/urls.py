from django.urls import path
from . import views

app_name = 'costos'

urlpatterns = [
    # Vista principal de gestión de costos
    path('', views.GestionCostosView.as_view(), name='gestion'),
    
    # Gestión de CostosViaje
    path('viajes-sin-costos/', views.ViajesSinCostosListView.as_view(), name='viajes_sin_costos'),
    path('crear/', views.CostosViajeCreateView.as_view(), name='crear'),
    
    # Registrar costos completo (debe estar antes de <int:pk>)
    path('viaje/<int:viaje_id>/registrar-completo/', views.registrar_costos_completo, name='registrar_completo'),
    path('viaje-ida-vuelta/<int:viaje_ida_id>/registrar/', views.registrar_ida_vuelta, name='registrar_ida_vuelta'),
    
    # Enviar formulario por email
    path('viaje/<int:viaje_id>/enviar-email/', views.enviar_formulario_email, name='enviar_email'),
    path('viaje-ida-vuelta/<int:viaje_ida_id>/enviar-email/', views.enviar_formulario_email_ida_vuelta, name='enviar_email_ida_vuelta'),
    
    # Mantenimientos y otros costos
    path('mantenimiento/<int:costos_pk>/', views.mantenimiento_costos, name='mantenimiento_costos'),
    path('otros-costos/<int:costos_pk>/', views.otros_costos, name='otros_costos'),
    
    # Peajes
    path('peaje/<int:pk>/eliminar/', views.PeajeDeleteView.as_view(), name='eliminar_peaje'),
    
    # CRUD de CostosViaje (deben estar después de las rutas específicas)
    path('<int:pk>/', views.CostosViajeDetailView.as_view(), name='detalle'),
    path('<int:pk>/editar/', views.CostosViajeUpdateView.as_view(), name='editar'),
    path('<int:pk>/eliminar/', views.CostosViajeDeleteView.as_view(), name='eliminar'),
    
    # Gestión de Puntos de Recarga
    path('<int:costos_pk>/punto-recarga/agregar/', views.agregar_puntos_recarga, name='agregar_punto'),
    path('punto-recarga/<int:pk>/editar/', views.PuntoRecargaUpdateView.as_view(), name='editar_punto'),
    path('punto-recarga/<int:pk>/eliminar/', views.PuntoRecargaDeleteView.as_view(), name='eliminar_punto'),
    
    # AJAX - Calcular distancia
    path('viaje/<int:viaje_id>/calcular-distancia/', views.calcular_distancia_viaje, name='calcular_distancia'),
    
    # Generar PDF
    path('viaje/<int:viaje_id>/formulario-pdf/', views.generar_formulario_costos_pdf, name='formulario_pdf'),
    path('informe-costos/<int:costos_pk>/', views.informe_costos_pdf, name='informe_costos_pdf'),

    # Registrar peajes y puntos de recarga
    path('registrar-peajes/<int:costos_pk>/', views.registrar_peajes, name='registrar_peajes'),
    path('registrar-puntos-recarga/<int:costos_pk>/', views.registrar_puntos_recarga, name='registrar_puntos_recarga'),

    # Registrar km inicial
    path('<int:costos_pk>/km-inicial/', views.registrar_km_inicial, name='registrar_km_inicial'),

    # Registrar km final
    path('<int:costos_pk>/km-final/', views.registrar_km_final, name='registrar_km_final'),
]
