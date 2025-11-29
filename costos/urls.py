from django.urls import path
from . import views

app_name = 'costos'

urlpatterns = [
    # Vista principal de gestión de costos
    path('', views.GestionCostosView.as_view(), name='gestion'),
    
    # Gestión de CostosViaje
    path('lista/', views.CostosViajeListView.as_view(), name='lista'),
    path('viajes-sin-costos/', views.ViajesSinCostosListView.as_view(), name='viajes_sin_costos'),
    path('crear/', views.CostosViajeCreateView.as_view(), name='crear'),
    path('<int:pk>/', views.CostosViajeDetailView.as_view(), name='detalle'),
    path('<int:pk>/editar/', views.CostosViajeUpdateView.as_view(), name='editar'),
    path('<int:pk>/eliminar/', views.CostosViajeDeleteView.as_view(), name='eliminar'),
    
    # Gestión de Puntos de Recarga
    path('<int:costos_pk>/punto-recarga/agregar/', views.PuntoRecargaCreateView.as_view(), name='agregar_punto'),
    path('punto-recarga/<int:pk>/editar/', views.PuntoRecargaUpdateView.as_view(), name='editar_punto'),
    path('punto-recarga/<int:pk>/eliminar/', views.PuntoRecargaDeleteView.as_view(), name='eliminar_punto'),
    
    # AJAX - Calcular distancia
    path('viaje/<int:viaje_id>/calcular-distancia/', views.calcular_distancia_viaje, name='calcular_distancia'),
    
    # Generar PDF
    path('viaje/<int:viaje_id>/formulario-pdf/', views.generar_formulario_costos_pdf, name='formulario_pdf'),
]
